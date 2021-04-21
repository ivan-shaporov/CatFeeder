#include <stdio.h>
#include <wiringPi.h>

#include "MotorController.h"

// http://wiringpi.com/pins/
#define Pin_Enable 8
#define Pin_Input1 7
#define Pin_Input2 9

#define ACTION_TIME 2000

int Init()
{
    int result = wiringPiSetup();
    pinMode(Pin_Enable, OUTPUT);
    pinMode(Pin_Input1, OUTPUT);
    pinMode(Pin_Input2, OUTPUT);
    return result;
}

void Test()
{
    printf("Pin_Input1\n");
    digitalWrite(Pin_Input1, HIGH);
    delay(3000);
    digitalWrite(Pin_Input1, LOW);

    printf("Pin_Input2\n");
    digitalWrite(Pin_Input2, HIGH);
    delay(3000);
    digitalWrite(Pin_Input2, LOW);

    printf("Pin_Enable\n");
    digitalWrite(Pin_Enable, HIGH);
    delay(3000);
    digitalWrite(Pin_Enable, LOW);
}

void RotateClockwise()
{
    digitalWrite(Pin_Input1, LOW);
    digitalWrite(Pin_Input2, HIGH);
    digitalWrite(Pin_Enable, HIGH);
}

void RotateCounterClockwise()
{
    digitalWrite(Pin_Input2, LOW);
    digitalWrite(Pin_Input1, HIGH);
    digitalWrite(Pin_Enable, HIGH);
}

void Stop()
{
    digitalWrite(Pin_Enable, LOW);
    digitalWrite(Pin_Input1, LOW);
    digitalWrite(Pin_Input2, LOW);
}

void Open()
{
    RotateClockwise();
    delay(ACTION_TIME);
    Stop();
}

void Close()
{
    RotateCounterClockwise();
    delay(ACTION_TIME);
    Stop();
}

void Feed()
{
    Init();
    Close();
    delay(1000);
    Open();
}