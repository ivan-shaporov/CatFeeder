#include <stdio.h>
#include <wiringPi.h>

#include "MotorController.h"

int main(void)
{
	/*int result = Init();
	printf("v1.0, result: %d\n", result);*/
	//Test();

	/*RotateClockwise();
	delay(2000);
	Stop();
	delay(1000);
	RotateCounterClockwise();
	delay(2000);
	Stop();*/

	/*Open();
	Close();*/

	for (size_t i = 0; i < 2; i++)
	{
		Feed();
		delay(5000);
	}
	return 0;
}
