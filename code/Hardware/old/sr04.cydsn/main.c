/* ========================================
CMPE 123 Project PSoC main file
By Scott Birss

Based on code from CMPE 121L by Scott Birss

*/

#include "project.h"

//used for debug
//function like leds are enabled
//#define DEBUG


#define PERIOD 0.0000000416666667 //in sec/cnt
#define FREQ 24 //000 in cycle per millsec
int cnt;
float time_var;
int time_millsec;
int cm;
float dis;
int toggle = 0;

//valid states: 
  //Parking spot taken == 0xF
  //Parking spot not taken == 0x0
  //Parking spot car moving == 0xA 
char prev_state;
char curr_state;

//less than this distance mean the car is parked
#define TRIG_DIS 100

CY_ISR(InterruptHandler){

    
    //clears the interrupt
    echo_ClearInterrupt();
    toggle = 0;
    
    //reads the length of the echo pin
    cnt = 4294967296 - Timer_1_ReadCounter();
    
    //converts into distance
    time_var = PERIOD * (float)cnt;
    time_millsec = cnt/FREQ;
    dis = time_var*2 * 34300; //dis in cm
    cm = time_millsec*2*34300;
    
    if(dis < TRIG_DIS) {
        curr_state = 0xF; //spot taken
        Control_Reg_Parking_Status_Write(0x1);
    } else if (dis < (TRIG_DIS + 100)) {
        curr_state = 0xA; //not sure if spot is taken
    } else {
        Control_Reg_Parking_Status_Write(0x0);
        curr_state = 0x0; //spot not taken
    }
    if(curr_state != prev_state) {
       Control_Reg_Parking_Status_Changed_Write(0x1);
       //CyDelay(500);
       //Control_Reg_Parking_Status_Changed_Write(0x0);
    }
    
    
//  #ifdef DEBUG
//    if(curr_state != prev_state) {
//        Led_Output_Write(0x1);
//        Led_Timer_Reset_Write(0x1);
//        Timer_3_Enable();
//    }
//  #endif
    
  prev_state = curr_state;
  


}


CY_ISR(SleepInt){
    SleepTimer_1_GetStatus();
    CyPmRestoreClocks();
    Control_Reg_Parking_Status_Changed_Write(0x0);

    //CyDelay(500);
    CyPmRestoreClocks();
    Timer_1_Wakeup();
    Timer_2_Wakeup();
    Timer_3_Wakeup();
    
    Timer_2_Enable();
    Control_Reg_1_Write(0x1);
    //CyDelay(800);
    toggle = 1;
    SleepTimer_1_DisableInt();
    //SleepTimer_1_Start();
}



int main(void)
{
    CyGlobalIntEnable; /* Enable global interrupts. */
    Timer_2_Start();
    Timer_1_Start();
    isr_1_StartEx(InterruptHandler); //start the interrupt
    isr_2_StartEx(SleepInt);
    //SleepTimer_1_EnableInt();
    //SleepTimer_1_Start();
    
    toggle = 0;
    Control_Reg_1_Write(0x0);
    
    CyDelay(10);

    Timer_3_Start();


    for(;;)
    {
        CyDelay(10);
        if (toggle == 0){
        toggle = 1;
        SleepTimer_1_EnableInt();
        SleepTimer_1_Start();
        Timer_1_Sleep();
        Timer_2_Sleep();
        Timer_3_Sleep();
        CyPmSaveClocks();
        CyPmSleep(PM_SLEEP_TIME_NONE, PM_SLEEP_SRC_CTW);
        }
        
//        CyPmRestoreClocks();
//        Timer_1_Wakeup();
//        Timer_2_Wakeup();
//        Timer_3_Wakeup();
//        
//        Timer_2_Enable();
//        Control_Reg_1_Write(0x1);
//        CyDelay(1000);
    }
}

/* [] END OF FILE */
