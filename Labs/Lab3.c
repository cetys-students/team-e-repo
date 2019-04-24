#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/debug.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"
#include "driverlib/pwm.h"
#include "driverlib/pin_map.h"

void delay()
{
    int Loop = 0;
    for(Loop = 0; Loop < 200; Loop++){
    }
}

int main(void)
{
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOC);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM1);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_PWM1)){
    }
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF)){
    }
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOC)){
    }
    //Set PORTC INPUT Pins
    GPIOPinTypeGPIOInput(GPIO_PORTC_BASE, (GPIO_PIN_4|GPIO_PIN_5|GPIO_PIN_6|GPIO_PIN_7));
    //Configure PF2 to be PWM5
    GPIOPinConfigure(GPIO_PF2_M1PWM6);
    //Configure PF3 to be PWM4
    GPIOPinConfigure(GPIO_PF3_M1PWM7);
    //Set PORTF.2 and PORTF.3 pin to be PWM
    GPIOPinTypePWM(GPIO_PORTF_BASE, GPIO_PIN_2);
    GPIOPinTypePWM(GPIO_PORTF_BASE, GPIO_PIN_3);
    PWMGenConfigure(PWM1_BASE, PWM_GEN_3, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    //32000 clock ticks to make a 50Hz PWM
    PWMGenPeriodSet(PWM1_BASE, PWM_GEN_3, 320000);
    //Link PWM generator 2 to PWM1 base
    PWMGenEnable(PWM1_BASE, PWM_GEN_3);
    //Set PWM to the rotation servo
    //Set PWM to the y-axis servo
    PWMOutputState(PWM1_BASE, (PWM_OUT_6_BIT|PWM_OUT_7_BIT), true);
    int up = 0;
    int down = 0;
    int right = 0;
    int left = 0;
    int ylimit = 26000;
    int xlimit = 26000;

    while(1){

        down = GPIOPinRead(GPIO_PORTC_BASE, GPIO_PIN_7);
        up = GPIOPinRead(GPIO_PORTC_BASE, GPIO_PIN_4);
        left = GPIOPinRead(GPIO_PORTC_BASE, GPIO_PIN_6);
        right = GPIOPinRead(GPIO_PORTC_BASE, GPIO_PIN_5);

        /*The established y-limit and x-limit ranges were calibrated
          according to the pan tilt dimensions*/
        if((down == GPIO_PIN_7) && (ylimit > 24222)){
            ylimit = ylimit - 1;
        }
        if((up == GPIO_PIN_4) && (ylimit < 40000)){
            ylimit = ylimit + 1;
        }
        if((left == GPIO_PIN_6) && (xlimit > 10000)){
            xlimit = xlimit - 1;
        }
        if((right == GPIO_PIN_5) && (xlimit < 42000)){
            xlimit = xlimit + 1;
        }

        PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6, xlimit);
        PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7, ylimit);
        delay();
    }
}

