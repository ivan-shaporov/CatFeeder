#include <stdio.h>
#include <bcm2835.h>

#include "MotorController.h"

//#define Pin_Enable RPI_V2_GPIO_P1_03
#define Pin_Input1 RPI_V2_GPIO_P1_07
#define Pin_Input2 RPI_V2_GPIO_P1_05

#define ACTION_TIME 1000

int Init()
{
    bcm2835_init();
    bcm2835_gpio_fsel(Pin_Input1, BCM2835_GPIO_FSEL_OUTP);
    bcm2835_gpio_fsel(Pin_Input2, BCM2835_GPIO_FSEL_OUTP);
    return 1;
}

void RotateClockwise()
{
    bcm2835_gpio_write(Pin_Input1, LOW);
    bcm2835_gpio_write(Pin_Input2, HIGH);
    // digitalWrite(Pin_Enable, HIGH);
}

void RotateCounterClockwise()
{
    bcm2835_gpio_write(Pin_Input2, LOW);
    bcm2835_gpio_write(Pin_Input1, HIGH);
    // digitalWrite(Pin_Enable, HIGH);
}

void Stop()
{
    // digitalWrite(Pin_Enable, LOW);
    bcm2835_gpio_write(Pin_Input1, LOW);
    bcm2835_gpio_write(Pin_Input2, LOW);
}

void Feed()
{
    Init();

    RotateCounterClockwise();
    delay(ACTION_TIME);
    Stop();

    delay(1000);

    RotateClockwise();
    delay(ACTION_TIME);
    Stop();

    bcm2835_close();
}