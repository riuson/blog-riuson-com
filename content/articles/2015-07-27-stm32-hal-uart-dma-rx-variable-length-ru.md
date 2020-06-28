Title: STM32 HAL UART DMA приём пакетов переменной длины
Tags: STM32

STM32 HAL UART Приём данных переменной длины с помощью DMA.
<!-- more -->

Добавляем определение обработчика для IDLE.
```diff
diff --git a/Drivers/STM32F1xx_HAL_Driver/Inc/stm32f1xx_hal_uart.h b/Drivers/STM32F1xx_HAL_Driver/Inc/stm32f1xx_hal_uart.h
--- a/Drivers/STM32F1xx_HAL_Driver/Inc/stm32f1xx_hal_uart.h
+++ b/Drivers/STM32F1xx_HAL_Driver/Inc/stm32f1xx_hal_uart.h
@@ -693,6 +693,7 @@ void HAL_UART_IRQHandler(UART_HandleTypeDef *huart);
 void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart);
 void HAL_UART_TxHalfCpltCallback(UART_HandleTypeDef *huart);
 void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart);
+void HAL_UART_RxIdleCallback(UART_HandleTypeDef *huart);
 void HAL_UART_RxHalfCpltCallback(UART_HandleTypeDef *huart);
 void HAL_UART_ErrorCallback(UART_HandleTypeDef *huart);
```

Добавляем обработку прерывания IDLE в обработчик прерываний UART.
```diff
diff --git a/Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_uart.c b/Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_uart.c
--- a/Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_uart.c
+++ b/Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_uart.c
@@ -1238,6 +1238,15 @@ void HAL_UART_IRQHandler(UART_HandleTypeDef *huart)
     UART_EndTransmit_IT(huart);
   }  
 
+  tmp_flag = __HAL_UART_GET_FLAG(huart, UART_FLAG_IDLE);
+  tmp_it_source = __HAL_UART_GET_IT_SOURCE(huart, UART_IT_IDLE);
+  /* UART in mode Transmitter end --------------------------------------------*/
+  if((tmp_flag != RESET) && (tmp_it_source != RESET))
+  {
+    __HAL_UART_CLEAR_IDLEFLAG(huart);
+    HAL_UART_RxIdleCallback(huart);
+  }
+
   if(huart->ErrorCode != HAL_UART_ERROR_NONE)
   {
     /* Set the UART state ready to be able to start again the process */
@@ -1248,6 +1257,19 @@ void HAL_UART_IRQHandler(UART_HandleTypeDef *huart)
 }
 
 /**
+  * @brief  Rx Idle callbacks.
+  * @param  huart: Pointer to a UART_HandleTypeDef structure that contains
+  *                the configuration information for the specified UART module.
+  * @retval None
+  */
+__weak void HAL_UART_RxIdleCallback(UART_HandleTypeDef *huart)
+{
+ /* NOTE: This function should not be modified, when the callback is needed,
+          the HAL_UART_RxIdleCallback can be implemented in the user file
+  */
+}
+
+/**
   * @brief  Tx Transfer completed callbacks.
   * @param  huart: Pointer to a UART_HandleTypeDef structure that contains
   *                the configuration information for the specified UART module.
```

Доработка задачи приёма.<br>
Настраивается приём через DMA для пакета размером в весь доступный буфер.<br>
Затем идёт ожидание семафора. Семафор устанавливается в обработчике IDLE.<br>
После, вычисляется количество принятых данных, как разница между ожидаемым количеством (размером буфера) и оставшимся (ещё не принятым) CNDTR.
```diff
diff --git a/Src/freertos.c b/Src/freertos.c
index a7db5b3..5ffd4df 100644
--- a/Src/freertos.c
+++ b/Src/freertos.c
@@ -38,13 +38,15 @@
 
 /* USER CODE BEGIN Includes */     
 #include "stm32f1xx_hal.h"
+#include <string.h>
 /* USER CODE END Includes */
 
 /* Variables -----------------------------------------------------------------*/
 osThreadId taskTestHandle;
 osThreadId taskSerialCommHandle;
 osThreadId taskDisplayHandle;
-osSemaphoreId semSerialCommReceivedHandle;
+osSemaphoreId semSerialCommRxIdleHandle;
+osSemaphoreId semSerialCommTxCompletedHandle;
 
 /* USER CODE BEGIN Variables */
 extern UART_HandleTypeDef huart1;
@@ -75,9 +77,13 @@ void MX_FREERTOS_Init(void) {
   /* USER CODE END RTOS_MUTEX */
 
   /* Create the semaphores(s) */
-  /* definition and creation of semSerialCommReceived */
-  osSemaphoreDef(semSerialCommReceived);
-  semSerialCommReceivedHandle = osSemaphoreCreate(osSemaphore(semSerialCommReceived), 1);
+  /* definition and creation of semSerialCommRxIdle */
+  osSemaphoreDef(semSerialCommRxIdle);
+  semSerialCommRxIdleHandle = osSemaphoreCreate(osSemaphore(semSerialCommRxIdle), 1);
+
+  /* definition and creation of semSerialCommTxCompleted */
+  osSemaphoreDef(semSerialCommTxCompleted);
+  semSerialCommTxCompletedHandle = osSemaphoreCreate(osSemaphore(semSerialCommTxCompleted), 1);
 
   /* USER CODE BEGIN RTOS_SEMAPHORES */
   /* add semaphores, ... */
@@ -126,10 +132,29 @@ void TaskTestStart(void const * argument)
 void TaskSerialCommStart(void const * argument)
 {
   /* USER CODE BEGIN TaskSerialCommStart */
+  int i, retval, rcvdCount;
+  /* Set semaphores to default state */
+  osSemaphoreWait(semSerialCommRxIdleHandle, osWaitForever);
+  osSemaphoreWait(semSerialCommTxCompletedHandle, osWaitForever);
   /* Infinite loop */
   for(;;)
   {
-    osDelay(1000);
+    uint8_t buffer[32];
+    memset(buffer, 0, sizeof(buffer));
+
+    __HAL_UART_CLEAR_IDLEFLAG(&huart1);
+    __HAL_UART_ENABLE_IT(&huart1, UART_IT_IDLE);
+    if (HAL_UART_Receive_DMA(&huart1, buffer, sizeof(buffer)) != HAL_OK) {
+      // error
+    }
+
+    retval = osSemaphoreWait(semSerialCommRxIdleHandle, osWaitForever);
+    rcvdCount = sizeof(buffer) - huart1.hdmarx->Instance->CNDTR;
+    HAL_UART_DMAStop(&huart1);
+
+    HAL_UART_Transmit_DMA(&huart1, buffer, rcvdCount);
+    retval = osSemaphoreWait(semSerialCommTxCompletedHandle, osWaitForever);
+    HAL_UART_DMAStop(&huart1);
   }
   /* USER CODE END TaskSerialCommStart */
 }
@@ -147,6 +172,21 @@ void TaslDisplayStart(void const * argument)
 }
 
 /* USER CODE BEGIN Application */
+void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart)
+{
+  osSemaphoreRelease(semSerialCommTxCompletedHandle);
+}
+
+void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
+{
+  osSemaphoreRelease(semSerialCommRxIdleHandle);
+}
+
+void HAL_UART_RxIdleCallback(UART_HandleTypeDef *huart)
+{
+  __HAL_UART_DISABLE_IT(huart, UART_IT_IDLE);
+  osSemaphoreRelease(semSerialCommRxIdleHandle);
+}
 /* USER CODE END Application */
```