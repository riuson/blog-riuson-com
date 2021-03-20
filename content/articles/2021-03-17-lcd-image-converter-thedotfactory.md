Title: LCD Image Converter - The Dot Factory
Date: 2021-03-17 22:45:00 +0500
Category: LCD Image Converter
Summary: Как сформировать шрифт, похожий на результат The Dot Factory.

## Как сформировать шрифт, похожий на результат The Dot Factory (далее TDF).

Генерируем в TDF шрифт с настройками по умолчанию.

Файл исходника (.c):
```c
// 
//  Font data for Ubuntu 8pt
// 

// Character bitmaps for Ubuntu 8pt
const uint_8 ubuntu_8ptBitmaps[] = 
{
	// @0 '0' (4 pixels wide)
	0x60, //  ## 
	0x90, // #  #
	0x90, // #  #
	0x90, // #  #
	0x90, // #  #
	0x90, // #  #
	0x90, // #  #
	0x60, //  ## 

	// @8 '1' (3 pixels wide)
	0x20, //   #
	0x60, //  ##
	0xA0, // # #
	0x20, //   #
	0x20, //   #
	0x20, //   #
	0x20, //   #
	0x20, //   #

	// @16 '2' (4 pixels wide)
	0x60, //  ## 
	0x90, // #  #
	0x10, //    #
	0x20, //   # 
	0x20, //   # 
	0x40, //  #  
	0x80, // #   
	0xF0, // ####

	// @24 '3' (4 pixels wide)
	0xE0, // ### 
	0x10, //    #
	0x10, //    #
	0x60, //  ## 
	0x10, //    #
	0x10, //    #
	0x10, //    #
	0xE0, // ### 
};

// Character descriptors for Ubuntu 8pt
// { [Char width in bits], [Offset into ubuntu_8ptCharBitmaps in bytes] }
const FONT_CHAR_INFO ubuntu_8ptDescriptors[] = 
{
	{4, 0}, 		// 0 
	{3, 8}, 		// 1 
	{4, 16}, 		// 2 
	{4, 24}, 		// 3 
};

// Font information for Ubuntu 8pt
const FONT_INFO ubuntu_8ptFontInfo =
{
	1, //  Character height
	'0', //  Start character
	'3', //  End character
	2, //  Width, in pixels, of space character
	ubuntu_8ptDescriptors, //  Character descriptor array
	ubuntu_8ptBitmaps, //  Character bitmap array
};

```

Заголовочный файл: (.h):

```c
// Font data for Ubuntu 8pt
extern const uint_8 ubuntu_8ptBitmaps[];
extern const FONT_INFO ubuntu_8ptFontInfo;
extern const FONT_CHAR_INFO ubuntu_8ptDescriptors[];
```

Для LIC создаём файл шаблона:

```cpp
$(start_block_header)
#include <stdint.h>

/*

// Character's info struct.
typedef struct FontTable {
  uint16_t    width; // Character's width.
  uint16_t    start; // Index of first character's byte.
} FONT_CHAR_INFO;

// Font's info struct.
typedef struct
{
  uint8_t Height;                  // Character's height.
  uint8_t FirstChar;               // First character.
  uint8_t LastChar;                // Last character.
  uint8_t FontSpace;               // Width of space character.
  const FONT_CHAR_INFO *FontTable; // Character descriptor array
  const uint8_t *FontBitmaps;      // Character bitmap array
} FONT_INFO;

*/
$(end_block_header)

// 
//  Font data for $(fnt_family) $(fnt_size)pt
// 

// Character bitmaps for $(fnt_family) $(fnt_size)pt
const uint$(img_data_block_size)_t $(doc_name_ws)_bitmaps[] = {
$(start_block_images_table)
    // at $(out_char_offset) '$(out_char_text)' #$(out_char_code)h ($(out_image_width) pixel(s) wide)
    $(out_image_preview)
    $(out_image_data)
#if ($(out_image_height) > 1)
	$(out_comma)
#endif
$(end_block_images_table)
};

// Character descriptors for $(fnt_family) $(fnt_size)pt
// { [Char width in bits], [Offset into $(doc_name_ws)_bitmaps in bytes] }
const FONT_CHAR_INFO $(doc_name_ws)_descriptors[] = {
$(start_block_images_table)
    { $(out_image_width), $(out_char_offset) } // '$(out_char_text)' #$(out_char_code)h
	$(out_comma)
$(end_block_images_table)
};

$(start_block_images_table)
#ifndef FIRST_CHAR
#define FIRST_CHAR '$(out_char_text)'
#endif

#ifdef LAST_CHAR
#undef LAST_CHAR
#endif

#define LAST_CHAR '$(out_char_text)'

#if (0x$(out_char_code) == 32)
#define SPACE_WIDTH $(out_image_height)
#endif
$(end_block_images_table)

// Space width by default.
#ifndef SPACE_WIDTH
#define SPACE_WIDTH 0
#endif

// Font information for $(fnt_family) $(fnt_size)pt
const FONT_INFO $(doc_name_ws)_FontInfo =
{
	($(out_images_max_height)/8) + ($(out_images_max_height)%8 == 0 ? 0 : 1), // Character height
	FIRST_CHAR,  // Start character
	LAST_CHAR,   // End character
	SPACE_WIDTH, // Width, in pixels, of space character
	$(doc_name_ws)_descriptors, // Character descriptor array
	$(doc_name_ws)_bitmaps,     // Character bitmap array
};

/*

Header file:

#ifndef $(doc_name_ws)_$(fnt_size)pt_H
#define $(doc_name_ws)_$(fnt_size)pt_H

// Font data for $(fnt_family) $(fnt_size)pt
extern const uint_8 $(doc_name_ws)_bitmaps[];
extern const FONT_INFO $(doc_name_ws)_FontInfo;
extern const FONT_CHAR_INFO $(doc_name_ws)_descriptors;

#endif // $(doc_name_ws)_$(fnt_size)pt_H
*/
```

Создаём шрифт, корректируем размеры, конвертируем с использованием этого шаблона.
Получаем:
```cpp

#include <stdint.h>

/*

// Character's info struct.
typedef struct FontTable {
  uint16_t    width; // Character's width.
  uint16_t    start; // Index of first character's byte.
} FONT_CHAR_INFO;

// Font's info struct.
typedef struct
{
  uint8_t Height;                  // Character's height.
  uint8_t FirstChar;               // First character.
  uint8_t LastChar;                // Last character.
  uint8_t FontSpace;               // Width of space character.
  const FONT_CHAR_INFO *FontTable; // Character descriptor array
  const uint8_t *FontBitmaps;      // Character bitmap array
} FONT_INFO;

*/


// 
//  Font data for Ubuntu 14pt
// 

// Character bitmaps for Ubuntu 14pt
const uint8_t Ubuntu_bitmaps[] = {

    // at 0 '0' #30h (8 pixel(s) wide)
    // ██∙∙∙∙██
    // █∙████∙█
    // █∙████∙█
    // █∙████∙█
    // █∙████∙█
    // █∙████∙█
    // █∙████∙█
    // █∙████∙█
    // █∙████∙█
    // ██∙∙∙∙██
    0xc3, 
    0xbd, 
    0xbd, 
    0xbd, 
    0xbd, 
    0xbd, 
    0xbd, 
    0xbd, 
    0xbd, 
    0xc3
#if (10 > 1)
	,
#endif

    // at 10 '1' #31h (8 pixel(s) wide)
    // ████∙███
    // ███∙∙███
    // ██∙█∙███
    // █∙██∙███
    // ████∙███
    // ████∙███
    // ████∙███
    // ████∙███
    // ████∙███
    // ████∙███
    0xf7, 
    0xe7, 
    0xd7, 
    0xb7, 
    0xf7, 
    0xf7, 
    0xf7, 
    0xf7, 
    0xf7, 
    0xf7
#if (10 > 1)
	,
#endif

    // at 20 '2' #32h (8 pixel(s) wide)
    // ██∙∙∙∙██
    // █∙████∙█
    // ██████∙█
    // ██████∙█
    // █████∙██
    // ████∙███
    // ███∙████
    // ██∙█████
    // █∙██████
    // █∙∙∙∙∙∙█
    0xc3, 
    0xbd, 
    0xfd, 
    0xfd, 
    0xfb, 
    0xf7, 
    0xef, 
    0xdf, 
    0xbf, 
    0x81
#if (10 > 1)
	
#endif

};

// Character descriptors for Ubuntu 14pt
// { [Char width in bits], [Offset into Ubuntu_bitmaps in bytes] }
const FONT_CHAR_INFO Ubuntu_descriptors[] = {

    { 8, 0 } // '0' #30h
	,

    { 8, 10 } // '1' #31h
	,

    { 8, 20 } // '2' #32h
	

};


#ifndef FIRST_CHAR
#define FIRST_CHAR '0'
#endif

#ifdef LAST_CHAR
#undef LAST_CHAR
#endif

#define LAST_CHAR '0'

#if (0x30 == 32)
#define SPACE_WIDTH 10
#endif

#ifndef FIRST_CHAR
#define FIRST_CHAR '1'
#endif

#ifdef LAST_CHAR
#undef LAST_CHAR
#endif

#define LAST_CHAR '1'

#if (0x31 == 32)
#define SPACE_WIDTH 10
#endif

#ifndef FIRST_CHAR
#define FIRST_CHAR '2'
#endif

#ifdef LAST_CHAR
#undef LAST_CHAR
#endif

#define LAST_CHAR '2'

#if (0x32 == 32)
#define SPACE_WIDTH 10
#endif


// Space width by default.
#ifndef SPACE_WIDTH
#define SPACE_WIDTH 0
#endif

// Font information for Ubuntu 14pt
const FONT_INFO Ubuntu_FontInfo =
{
	(10/8) + (10%8 == 0 ? 0 : 1), // Character height
	FIRST_CHAR,  // Start character
	LAST_CHAR,   // End character
	SPACE_WIDTH, // Width, in pixels, of space character
	Ubuntu_descriptors, // Character descriptor array
	Ubuntu_bitmaps,     // Character bitmap array
};

/*

Header file:

#ifndef Ubuntu_14pt_H
#define Ubuntu_14pt_H

// Font data for Ubuntu 14pt
extern const uint_8 Ubuntu_bitmaps[];
extern const FONT_INFO Ubuntu_FontInfo;
extern const FONT_CHAR_INFO Ubuntu_descriptors;

#endif // Ubuntu_14pt_H
*/
```

Нюансы:

TDF добавляет в шрифт, помимо используемых символов, также и все остальные между первым и последним, что даёт возмоджность обращаться к ним по индексу.
Для решения проблемы перерасхода памяти из-за этого, TDF имеет опцию разбиения набора символов на отдельные блоки.

В LIC это не предусмотрено, в результирующий шрифт встраиваются только заранее добавленные символы. А выборка нужного производится алгоритмом [бинарного поиска](https://ru.wikipedia.org/wiki/%D0%94%D0%B2%D0%BE%D0%B8%D1%87%D0%BD%D1%8B%D0%B9_%D0%BF%D0%BE%D0%B8%D1%81%D0%BA).

Возможно создать непрерывную последовательность символов, добавив их все. А чтобы ненужные занимали меньше места в памяти, устанавливаем им размеры 1*1 пиксел и исключаем по этому признаку с помощью макросов.
