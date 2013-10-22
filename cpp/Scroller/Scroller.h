#include <windowsx.h>
#include <math.h>
#pragma comment(lib, "Msimg32.lib") // Für TransparentBlt


class Scroller
{
public:
	Scroller(HDC TargetHDC, BitmapFont *bitmapFont, int scrollerWidth, char *Text);
	~Scroller();

	void Move();
	void Draw(int xPos, int yPos);
	HDC getBackbufferDC();

private:
	HDC hOutDC; //Hier wird am Ende drauf gezeichnet.

	HDC hScrollerDC;
	HBITMAP hScrollerCanvas;
	BitmapFont *bitmapFont;
	char *Text;

	int scrollerDimX;
	int scrollerDimY;
	int scrollDelay;
	int TextPos;
	int BlitSpace; //Nicht sichtbarer bereich in dem die Buchstaben geblittet werden.
};


class SineEffectCanvas
{
public:
	SineEffectCanvas(int canvasDimX, int canvasDimY, int Amplitude = 40, int Frequenz = 6);
	~SineEffectCanvas();

	void Draw(HDC hInDC, HDC hOutDC, int xPos, int yPos, bool transparent = false, COLORREF TransparentColor = RGB(0x255, 0x0, 0x255));

private:
	HDC hEffectDC;
	HBITMAP hEffectCanvas;

	int canvasDimX;
	int canvasDimY;
	int Amplitude;
	int Frequenz;

	float scrollsinus1;
	float scrollsinus2;
};

//TODO: Scroller und SineEffectCanvas zu einem Objekt zusammenfassen!
class SineScroller
{

};