//#include "StdAfx.h"
#include <BitmapFont/BitmapFont.h>
#include <Scroller/Scroller.h>

Scroller::Scroller(HDC TargetHDC, BitmapFont *bitmapFont, int scrollerWidth, char *Text)
{
	this->hOutDC = TargetHDC;
	this->scrollDelay = 0;
	this->scrollerDimX = scrollerWidth;
	this->scrollerDimY = bitmapFont->getLettersHeight();
	this->bitmapFont = bitmapFont;
	this->Text = Text;
	this->TextPos = 0;
	this->BlitSpace = bitmapFont->getLetterWidth('Z');

	//Scroller Grafikbereich anlegen
	hScrollerDC = CreateCompatibleDC(TargetHDC);
	hScrollerCanvas = CreateCompatibleBitmap(TargetHDC, scrollerDimX, scrollerDimY);
	HBITMAP hOld = SelectBitmap(hScrollerDC, hScrollerCanvas);
	DeleteObject(hOld);
}


Scroller::~Scroller()
{
	DeleteObject(hScrollerCanvas);
	DeleteDC(hScrollerDC);
}

//Scroller um einen Pixel nach links verschieben.
void Scroller::Move()
{
	//Ist es zeit für nen neuen Buchstaben?
	if(scrollDelay == 0)
	{
		bitmapFont->ZeichneBuchstabe(hScrollerDC, Text[TextPos], scrollerDimX-bitmapFont->getLetterWidth(Text[TextPos])-1, 0);
		TextPos++;
		
		//Wenn Text zu ende ist, von vorne anfangen.
		if(Text[TextPos] == 0)
			TextPos = 0;
		
		scrollDelay = bitmapFont->getLetterWidth(Text[TextPos]);
	}

	BitBlt(hScrollerDC, 0, 0, scrollerDimX+BlitSpace, scrollerDimY, hScrollerDC, 1, 0, SRCCOPY);
	scrollDelay--;
}

void Scroller::Draw(int xPos, int yPos)
{
	Move();

	//Scroller blitten
	BitBlt(hOutDC, xPos, yPos, scrollerDimX-BlitSpace, scrollerDimY, hScrollerDC, 0, 0, SRCCOPY);
}

HDC Scroller::getBackbufferDC()
{
	return hScrollerDC;
}


SineEffectCanvas::SineEffectCanvas(int canvasDimX, int canvasDimY, int Amplitude, int Frequenz)
{
	this->canvasDimX = canvasDimX;
	this->canvasDimY = canvasDimY;
	this->scrollsinus1 = 0;
	this->scrollsinus2 = 0;
	this->Amplitude = Amplitude;
	this->Frequenz  = Frequenz;

	//Effekt Grafikbereich anlegen
	HDC desktopDC = GetDC(0);
	hEffectDC = CreateCompatibleDC(NULL);
	hEffectCanvas = CreateCompatibleBitmap(desktopDC, canvasDimX, canvasDimY);
	HBITMAP hOld = SelectBitmap(hEffectDC, hEffectCanvas);
	DeleteObject(hOld);
}

SineEffectCanvas::~SineEffectCanvas()
{

}


void SineEffectCanvas::Draw(HDC hInDC, HDC hOutDC, int xPos, int yPos, bool transparent, COLORREF TransparentColor)
{
	int A = this->Amplitude;
	float f = this->Frequenz/100.0f;

	// 2-Pixel Sinescroll	
	// Take the standard scroller in the background as source and blit it to the front screen
	// Blitting in 250 steps, changing y coord so we have a sinewave
	int i=0;
	PatBlt(hEffectDC, 0, 0, canvasDimX, canvasDimY, 0);

	
	for (i=0, scrollsinus2=scrollsinus1; i<canvasDimX; i+=2) 
	{	
		BitBlt(hEffectDC, i, A + int(A*sin(scrollsinus2)), 2, canvasDimY, hInDC, i, 0, SRCCOPY);
		scrollsinus2+=.022f;
	}	

	// Blit entire backbuffer to frontscreen
	if(!transparent)
		BitBlt(hOutDC, xPos, yPos, canvasDimX, canvasDimY, hEffectDC, 0, 0, SRCCOPY);
	else
		TransparentBlt(hOutDC, xPos, yPos, canvasDimX, canvasDimY, hEffectDC, 0, 0, canvasDimX, canvasDimY, TransparentColor);

	scrollsinus1 += f; //.06f;
}
