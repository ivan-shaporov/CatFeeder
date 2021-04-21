// gcc -l rt exp.c -l bcm2835 -o exp

#include <bcm2835.h>
#include <stdio.h>

#define PIN RPI_GPIO_P1_07

int main(int argc, char **argv)
{
    printf("test\n");
    // If you call this, it will not actually access the GPIO
    // Use for testing
//    bcm2835_set_debug(1);

    if (!bcm2835_init())
        return 1;

    bcm2835_gpio_fsel(PIN, BCM2835_GPIO_FSEL_OUTP);

    while (1)
    {
        bcm2835_gpio_write(PIN, HIGH);

        bcm2835_delay(1500);

        bcm2835_gpio_write(PIN, LOW);

        bcm2835_delay(1500);
    }
    bcm2835_close();
    return 0;
}