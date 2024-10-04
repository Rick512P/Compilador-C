#include <stdio.h>

#define TAMANHO 20

void quicksort(int vetor[], int inicio, int fim) {
    if (inicio < fim) {
        int pivo = vetor[fim];  
        int i = inicio - 1;
       
        for (int j = inicio; j < fim; j++) {
            if (vetor[j] < pivo) {
                i++;                
                int temp = vetor[i];
                vetor[i] = vetor[j];
                vetor[j] = temp;
            }
        }
        
        int temp = vetor[i + 1];
        vetor[i + 1] = vetor[fim];
        vetor[fim] = temp;

        int pi = i + 1;  
        
        quicksort(vetor, inicio, pi - 1);
        quicksort(vetor, pi + 1, fim);
    }
}

int main() {    
    int vetor[TAMANHO] = {17, 1, 12, 18, 8, 9, 6, 13, 15, 3, 20, 7, 14, 4, 16, 0, 11, 19, 10, 5}
    
    printf("Vetor antes da ordenacao:\n");
    for (int i = 0; i < TAMANHO; i++) {
        printf("%d ", vetor[i]);
    }
    printf("\n");

    quicksort(vetor, 0, TAMANHO - 1);

    printf("Vetor apos a ordenacao:\n");
    for (int i = 0; i < TAMANHO; i++) {
        printf("%d ", vetor[i]);
    }
    printf("\n");
    return 0;
}
