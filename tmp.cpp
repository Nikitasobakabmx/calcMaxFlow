#include "RTE_Components.h"
#include CMSIS_device_header
#include <stdio.h>

int main()
{
	SystemCoreClockUpdate();
	ITM_SendChar('\n');
	printf("Start clk=%d Hz\n",SystemCoreClock);
	volatile uint32_t StartUpCounter = 0, HSIStatus = 0;
	SET_BIT(RCC->CR,RCC_CR_HSION);// HSI ON
	do {
		HSIStatus = RCC->CR & RCC_CR_HSIRDY;
		StartUpCounter++;
	} while((HSIStatus == 0) && (StartUpCounter != 0x5000));

	if ((RCC->CR & RCC_CR_HSIRDY) != RESET) //HSI
	{
		FLASH->ACR = FLASH_ACR_PRFTBE|FLASH_ACR_LATENCY_0;
		RCC->CFGR |= RCC_CFGR_HPRE_0;

		CLEAR_BIT(RCC -> CR,RCC_CR_PLLON); // Turn off PLL
		//Clear PLLSRC,PLLXTPRE,PLLMULL bits
		RCC->CFGR &= ~(RCC_CFGR_PLLSRC | RCC_CFGR_PLLXTPRE | RCC_CFGR_PLLMULL);
		//Setting PLLSRC 	- HSI
		//				PLLMULL - PLLMULL5
		RCC->CFGR |= (RCC_CFGR_PLLSRC_HSI_Div2 | RCC_CFGR_PLLMULL5);
		SET_BIT(RCC -> CR,RCC_CR_PLLON); // Turn onn PLL

		while((RCC->CR,RCC_CR_PLLON)==RESET){}

		RCC->CFGR &= ~(RCC_CFGR_SW); 
		RCC->CFGR |= RCC_CFGR_SW_PLL;

		while((RCC->CFGR & RCC_CFGR_SWS) != RCC_CFGR_SWS_PLL){}
	}
	else
	{ 
		while(1){} 
	}

	SystemCoreClockUpdate(); // Update SystemCoreClock value
	printf("After configuration clk=%d Hz\n",SystemCoreClock);

	SET_BIT(RCC->CFGR, RCC_CFGR_MCO_SYSCLK);

	SET_BIT(RCC->APB2ENR,RCC_APB2ENR_IOPAEN | RCC_APB2ENR_IOPBEN);
	GPIOA->CRH &= ~(GPIO_CRH_MODE8 | GPIO_CRH_CNF8);
	GPIOA->CRL &= ~(GPIO_CRL_MODE4 | GPIO_CRL_CNF4);
	GPIOB->CRL &= ~(GPIO_CRL_MODE5 | GPIO_CRL_CNF5);


	SET_BIT(GPIOA->CRH,GPIO_CRH_MODE8|GPIO_CRH_CNF8_1);

	SET_BIT(GPIOA->CRL,GPIO_CRL_MODE4);  //Hight speed
	SET_BIT(GPIOB->CRL,GPIO_CRL_MODE5_1);//Low 	 speed


	while(1)
	{
		GPIOA->BSRR = GPIO_BSRR_BS4;
		GPIOB->BSRR = GPIO_BSRR_BS5;

		GPIOA->BRR = GPIO_BRR_BR4;  
		GPIOB->BRR = GPIO_BRR_BR5;  
	}
}
