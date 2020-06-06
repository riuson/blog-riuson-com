{
  "title": "Creating image for STM32 Discovery BSP",
  "date": "2016-09-18 15:50:00 +0500",
  "categories": [ "STM32" ],
  "excerpt": "How to create an image in С format for using with STM32F429I-Disco and same boards with BSP (Board Support Package)."
}

## Initial data

And once there was a question ... How do I create an image for the board STM32F429I-Disco in "C" format for use with the <abbr title="Board Support Package">BSP</abbr>?

```cpp
#ifndef __STLOGO_H
#define __STLOGO_H

#if defined ( __ICCARM__ ) /*!< IAR Compiler */
  #pragma data_alignment=4   
#endif

__ALIGN_BEGIN const  unsigned char stlogo[9174] __ALIGN_END =
{
0x42,0x4d,0xd6,0x23,0x00,0x00,0x00,0x00,0x00,0x00,0x36,0x00,0x00,0x00,0x28,0x00,
0x00,0x00,0x50,0x00,0x00,0x00,0x39,0x00,0x00,0x00,0x01,0x00,0x10,0x00,0x03,0x00,
0x00,0x00,0xa0,0x23,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
...
```


## Data format

After examining the code section of the above, it became clear that this header structure [BMP format](https://en.wikipedia.org/wiki/BMP_file_format).
I think it was made for ease of use the image files from the SD memory card.

Also, based on the code of function `void BSP_LCD_DrawBitmap(uint32_t X, uint32_t Y, uint8_t *pBmp)` from file `stm32f429i_discovery_lcd.c` it can be assumed that code supports only the following data formats: A8R8G8B8, R5G6B5 and R8G8B8.

How can I display an image in this format?

There is a ready tool Bitmap Converter for emWin (BmpCvt.exe), which comes in STemwin package. You can certainly try it, but it's a simple way.

How to make the conversion using LCD Image Converter?

The simplest - is to decide that the conversion is not possible, as there is no ready-made presets for this.
However, the problem is only in the reconstruction of the structure header BMP and filling them with the right data.

From Wiki article mentioned above, we can obtain the following structure:
```cpp
typedef struct tagBITMAPFILEHEADER {
  uint16_t   bfType; // File type, 'BM', little-endian.
  uint32_t   bfSize; // Size of file, in bytes.
  uint16_t   bfReserved1;
  uint16_t   bfReserved2;
  uint32_t   bfOffBits; // Offset of pixel's data from file's start.
} BITMAPFILEHEADER; // 14 bytes

// Версия 3, BITMAPINFOHEADER.
typedef struct tagBITMAPINFOHEADER {
  uint32_t  biSize; // Size of this structure and its version.
  int32_t   biWidth; // Width of image, must be freater than 0.
  int32_t   biHeight; // Height of image, must be freater than 0.
  uint16_t  biPlanes; // Number of planes, must be equals to 1.
  uint16_t  biBitCount; // Count of bits per pixel.
  uint32_t  biCompression; // Compression type. At ST's file it equals to 3, but not used because biClrUsed == 0.
  uint32_t  biSizeImage; // Size of image's data, in bytes.
  int32_t   biXPelsPerMeter; // Equals to 0.
  int32_t   biYPelsPerMeter; // Equals to 0.
  uint32_t  biClrUsed; // Equals to 0.
  uint32_t  biClrImportant; // Equals to 0.
} BITMAPINFOHEADER; // 40 bytes
```

## Template

Colors will be stored in R5G6B5 format, ie 16 bits.
For this purpose, it is more convenient to take as a storage unit `uin16_t`, instead `uint8_t`, which will affect the data in the header.


Template for filling such a structure, for the GCC compiler, will be as follows:
```cpp
#ifndef $(doc_name_ws)_H_
#define $(doc_name_ws)_H_

#include <stdint.h>

// struct packing, pragma for GCC !!!
#pragma pack(push, 1)

$(start_block_images_table)

typedef struct $(doc_name_ws)_tagBITMAPFILEHEADER {
  uint16_t   bfType;
  uint32_t   bfSize;
  uint16_t   bfReserved1;
  uint16_t   bfReserved2;
  uint32_t   bfOffBits;
} $(doc_name_ws)_BITMAPFILEHEADER; // size is 14 bytes

typedef struct $(doc_name_ws)_tagBITMAPINFOHEADER {
  uint32_t  biSize;
  uint32_t  biWidth;
  uint32_t  biHeight;
  uint16_t  biPlanes;
  uint16_t  biBitCount;
  uint32_t  biCompression;
  uint32_t  biSizeImage;
  uint32_t  biXPelsPerMeter;
  uint32_t  biYPelsPerMeter;
  uint32_t  biClrUsed;
  uint32_t  biClrImportant;
} $(doc_name_ws)_BITMAPINFOHEADER; // size is 40 bytes

typedef struct $(doc_name_ws)_tag_Struct {
  // offset 0, size 14
  $(doc_name_ws)_BITMAPFILEHEADER fileHeader;
  // offset 14, size 40
  $(doc_name_ws)_BITMAPINFOHEADER infoHeader;
  // offset 54, size $(out_blocks_count) words
  uint16_t data[$(out_blocks_count)];
} $(doc_name_ws)_Struct;


$(doc_name_ws)_Struct $(doc_name_ws) = {
  {
    0x4d42u,
    sizeof($(doc_name_ws)_BITMAPINFOHEADER) + sizeof($(doc_name_ws)_BITMAPFILEHEADER) + ($(out_blocks_count) * 2),
    0x0000u,
    0x0000u,
    sizeof($(doc_name_ws)_BITMAPINFOHEADER) + sizeof($(doc_name_ws)_BITMAPFILEHEADER)
  },
  {
    sizeof($(doc_name_ws)_BITMAPINFOHEADER),
    $(out_image_width),
    $(out_image_height),
    1u,
    $(out_bpp),
    0x00000003u,
    ($(out_blocks_count) * 2),
    0x00000000ul,
    0x00000000ul,
    0x00000000ul,
    0x00000000ul
  },
  {
  $(out_image_data)
  }
};

$(end_block_images_table)

// struct packing, pragma for GCC !!!
#pragma pack (pop)



#endif /* $(doc_name_ws)_H_ */
```

## Settings

Main window of application

![LCD Image Converter main window](assets/images/posts/2016/09/18/generate-image-for-stm32-discovery-bsp-1.png){ .img-fluid }

Prepare.

![Options - Conversion - Prepare](assets/images/posts/2016/09/18/generate-image-for-stm32-discovery-bsp-2.png){ .img-fluid }

Color's matrix for R5G6B5.

![Options - Conversion - Matrix](assets/images/posts/2016/09/18/generate-image-for-stm32-discovery-bsp-3.png){ .img-fluid }

Image.

![Options - Conversion - Image](assets/images/posts/2016/09/18/generate-image-for-stm32-discovery-bsp-4.png){ .img-fluid }

Template file.

![Options - Conversion - Templates](assets/images/posts/2016/09/18/generate-image-for-stm32-discovery-bsp-5.png){ .img-fluid }

## Results

```cpp
#ifndef butterfly_H_
#define butterfly_H_

#include <stdint.h>

// struct packing, pragma for GCC !!!
#pragma pack(push, 1)



typedef struct butterfly_tagBITMAPFILEHEADER {
  uint16_t   bfType;
  uint32_t   bfSize;
  uint16_t   bfReserved1;
  uint16_t   bfReserved2;
  uint32_t   bfOffBits;
} butterfly_BITMAPFILEHEADER; // size is 14 bytes

typedef struct butterfly_tagBITMAPINFOHEADER {
  uint32_t  biSize;
  uint32_t  biWidth;
  uint32_t  biHeight;
  uint16_t  biPlanes;
  uint16_t  biBitCount;
  uint32_t  biCompression;
  uint32_t  biSizeImage;
  uint32_t  biXPelsPerMeter;
  uint32_t  biYPelsPerMeter;
  uint32_t  biClrUsed;
  uint32_t  biClrImportant;
} butterfly_BITMAPINFOHEADER; // size is 40 bytes

typedef struct butterfly_tag_Struct {
  // offset 0, size 14
  butterfly_BITMAPFILEHEADER fileHeader;
  // offset 14, size 40
  butterfly_BITMAPINFOHEADER infoHeader;
  // offset 54, size 76800 words
  uint16_t data[76800];
} butterfly_Struct;


butterfly_Struct butterfly = {
  {
    0x4d42u,
    sizeof(butterfly_BITMAPINFOHEADER) + sizeof(butterfly_BITMAPFILEHEADER) + (76800 * 2),
    0x0000u,
    0x0000u,
    sizeof(butterfly_BITMAPINFOHEADER) + sizeof(butterfly_BITMAPFILEHEADER)
  },
  {
    sizeof(butterfly_BITMAPINFOHEADER),
    240,
    320,
    1u,
    16,
    0x00000003u,
    (76800 * 2),
    0x00000000ul,
    0x00000000ul,
    0x00000000ul,
    0x00000000ul
  },
  {
    0x19e2, 0x2202, 0x2202, 0x2242, 0x2262, 0x2262, 0x2ac3, 0x3b64, 0x3ba4, 0x3b84, 0x4ba5, 0x4bc5, 0x3b85, 0x3304, 0x2ac3, 0x2aa3, 0x2aa3, 0x2aa3, 0x2283, 0x2a83, 0x2aa3, 0x2aa3, 0x2ac3, 0x2ae3, 0x3324, 0x3b84, 0x43c5, 0x43e5, 0x4405, 0x4405, 0x4405, 0x4405, 0x4405, 0x4405, 0x4405, 0x43e4, 0x3363, 0x2262, 0x1942, 0x1102, 0x1102, 0x1102, 0x1102, 0x1922, 0x1942, 0x1962, 0x1962, 0x1942, 0x1942, 0x1922, 0x1902, 0x1902, 0x1922, 0x1943, 0x1963, 0x1983, 0x1963, 0x1943, 0x1943, 0x1922, 0x1922, 0x1943, 0x1963, 0x1983, 0x2163, 0x1963, 0x1922, 0x1102, 0x1982, 0x2222, 0x2b22, 0x43a4, 0x5445, 0x5466, 0x5c86, 0x5c86, 0x43a3, 0x2202, 0x08a1, 0x1081, 0x1081, 0x1081, 0x10a2, 0x18e3, 0x2103, 0x2123, 0x29a3, 0x2a23, 0x2263, 0x2283, 0x2aa3, 0x22a3, 0x2aa3, 0x22a3, 0x2ac3, 0x22c3, 0x2ac3, 0x2ac3, 0x2ac3, 0x2243, 0x1983, 0x18e2, 0x18c2, 0x18e3, 0x18e2, 0x1903, 0x18e2, 0x10e2, 0x10e2, 0x10e2, 0x10c2, 0x10a1, 0x10a1, 0x10c2, 0x10e2, 0x1102, 0x1902, 0x1902, 0x18e2, 0x18e2, 0x18e2, 0x1102, 0x1922, 0x1942, 0x1942, 0x1942, 0x1943, 0x1922, 0x1102, 0x10c2, 0x10a2, 0x10c2, 0x10c2, 0x10c2, 0x10e2, 0x1902, 0x1922, 0x1962, 0x19a3, 0x19c3, 0x19a3, 0x19a3, 0x21a3, 0x19c3, 0x19c3, 0x19c3, 0x19e3, 0x22a3, 0x43c6, 0x5c88, 0x64c9, 0x64c9, 0x64ca, 0x64ca, 0x64aa, 0x5caa, 0x5caa, 0x5caa, 0x5cc9, 0x5cca, 0x5caa, 0x5ca9, 0x64a9, 0x5c87, 0x43a4, 0x2ac2, 0x19c2, 0x21c2, 0x19a2, 0x1982, 0x1982, 0x1962, 0x1982, 0x22c1, 0x43c4, 0x6486, 0x64c8, 0x64c9, 0x5cc9, 0x5ca8, 0x54a8, 0x5488, 0x54a8, 0x54c8, 0x5cc8, 0x5c87, 0x43e4, 0x2ae2, 0x1a42, 0x2282, 0x22a2, 0x2b23, 0x43e4, 0x5445, 0x4c04, 0x3323, 0x1a02, 0x1102, 0x1902, 0x1963, 0x2223, 0x3304, 0x4385, 0x4c06, 0x5426, 0x5466, 0x64a6, 0x6ce6, 0x6d07, 0x7526, 0x6d26, 0x6d26, 0x6d26, 0x6d26, 0x6d06, 0x6d07, 0x5cc8, 0x5488, 0x5469, 0x5468, 0x4c68, 0x5448, 0x4c68, 0x5468, 0x5468, 0x5468, 0x4c68, 0x4c47, 0x4c68, 0x5448, 0x4c48, 0x4c27, 0x4c27, 0x4c27, 0x4c27, 0x4c27, 0x4406, 0x4407, 0x43e6, 0x3ba6,
    ...
    0x64c0, 0x5c81, 0x43c1, 0x2b22, 0x2222, 0x1a22, 0x2242, 0x2243, 0x21e2, 0x1982, 0x1922, 0x10e2, 0x10e2, 0x10e2, 0x10e2, 0x10e2, 0x1942, 0x2223, 0x2ae3, 0x3b44, 0x4bc5, 0x6487, 0x6d29, 0x758a, 0x7d8a, 0x7daa, 0x7daa, 0x85ca, 0x85eb, 0x8deb, 0x8e0c, 0x85ec, 0x7dec, 0x85ec, 0x8e0c, 0x962c, 0x962c, 0x962c, 0x8e2c, 0x8e0c, 0x85ec, 0x85cc, 0x85ed, 0x960d, 0x962d, 0x960d, 0x8dcc, 0x858b, 0x7d4b, 0x752a, 0x752a, 0x6d29, 0x7509, 0x6d09, 0x6d09, 0x7509, 0x6ce8, 0x6487, 0x5446, 0x43e5, 0x3b84, 0x3364, 0x3344, 0x3344, 0x2b44, 0x3344, 0x3344, 0x3b85, 0x43e6, 0x4c27, 0x5c68, 0x5c88, 0x5c88, 0x5c67, 0x5427, 0x4bc5, 0x4364, 0x32a3, 0x2a03, 0x2983, 0x2963, 0x2963, 0x2122, 0x18e2, 0x1902, 0x1922, 0x3204, 0x4245, 0x4a65, 0x4244, 0x29c3, 0x1922, 0x10e2, 0x10a2, 0x2182, 0x4322, 0x6443, 0x7504, 0x7d84, 0x7da5, 0x7dc5, 0x7dc6, 0x7de6, 0x7dc6, 0x7de6, 0x7dc6, 0x7dc6, 0x7de7, 0x8608, 0x8e49, 0x9689, 0x9688, 0x9688, 0x8e68, 0x8e68, 0x85c7, 0x6d05, 0x4c03, 0x2b02, 0x3323, 0x4bc5, 0x6486, 0x7507, 0x8588, 0x8da8, 0x9609, 0x9628, 0x9628, 0x9648, 0x9648, 0x9668, 0x9688, 0x9668, 0x9648, 0x9648, 0x9629, 0x8587, 0x6cc6, 0x53e4, 0x4304, 0x4303, 0x3b23, 0x3b23, 0x3ac3, 0x3a43, 0x3a23, 0x31e3, 0x21c2, 0x21e2, 0x21e2, 0x2182, 0x1922, 0x10c2, 0x1081, 0x0861, 0x0861, 0x0861, 0x0861, 0x0841, 0x1081, 0x10c2, 0x1922, 0x1982, 0x21c2, 0x21e2, 0x2202, 0x2222, 0x2242, 0x2242, 0x2262, 0x2262, 0x2262, 0x2262, 0x2262, 0x2262, 0x2262, 0x2242, 0x2222, 0x21a3, 0x1922, 0x10c2, 0x1061, 0x0861, 0x0841, 0x0841, 0x0841, 0x0020, 0x0020, 0x0000, 0x0020, 0x0020, 0x0020, 0x0020, 0x0020, 0x0020, 0x0841, 0x1081, 0x1942, 0x5424, 0x8dc8, 0x85c9, 0x7d8a, 0x756a, 0x754b, 0x6d4a, 0x756b, 0x756b, 0x756b, 0x756b, 0x756a, 0x756a, 0x756a, 0x754b, 0x756a, 0x758a, 0x756a, 0x758a, 0x7d6b, 0x7d6c, 0x856d, 0x7d6d, 0x756c, 0x756c, 0x756c, 0x754b, 0x754a, 0x756b, 0x756b, 0x758b, 0x758b, 0x7d8b, 0x758b, 0x758b, 0x7d8b, 0x7d6c, 0x8dcd, 0xa60f, 0x8d8f, 0x752c, 0x6d2b
  }
};

// struct packing, pragma for GCC !!!
#pragma pack (pop)

#endif /* butterfly_H_ */
```

![Photo of board STM32F429I-Disco with image](assets/images/posts/2016/09/18/generate-image-for-stm32-discovery-bsp-6.png){ .img-fluid }
