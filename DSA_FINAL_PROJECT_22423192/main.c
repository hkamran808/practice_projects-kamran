#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "dsa_final_project.h"

void displayMenu() {
    printf("---------- EATCoin menu ----------\n");
    printf("1.show the list of blocks in the BlockChain\n");
    printf("2.show all transactions in a block\n");
    printf("3.show all transactions for a student on a given day\n");
    printf("4.show the history for a student\n");
    printf("5.credit an account\n");
    printf("6.pay for a meal\n");
    printf("7.transfer EATCoins between two students\n");
    printf("8.export transactions to a file\n");
    printf("9.import transactions from a file\n");
    printf("10.EXIT\n");
    printf("choose an option: ");
}

int main() {
    BlockChain bc = NULL;
    int choice;
    int studentID, sourceID, destID, blockID, date;
    float amount;
    char description[100];
    char filename[100];
    
    printf("welcome to our EATCoin management project!!!\n");
    
    bc = addBlock(bc);
    
    do {
        displayMenu();
        scanf("%d", &choice);
        
        switch (choice) {
            case 1:
                displayBlockChain(bc);
                break;
                
            case 2:
                printf("enter block ID: ");
                scanf("%d", &blockID);
                {
                    T_Block *current = bc;
                    while (current != NULL) {
                        if (current->blockID == blockID) {
                            displayBlockTransactions(*current);
                            break;
                        }
                        current = current->next;
                    }
                    if (current == NULL) {
                        printf("block with ID %d NOT found!!!\n", blockID);
                    }
                }
                break;
                
            case 3:
                printf("enter student ID: ");
                scanf("%d", &studentID);
                printf("Enter date (as YYYYMMDD): ");
                scanf("%d", &date);
                displayStudentDailyTransactions(studentID, date, bc);
                break;
                
            case 4:
                printf("Enter student ID: ");
                scanf("%d", &studentID);
                consult(studentID, bc);
                break;
                
            case 5:
                printf("enter student ID: ");
                scanf("%d", &studentID);
                printf("enter amount to credit: ");
                scanf("%f", &amount);
                printf("enter description: ");
                getchar();
                fgets(description, sizeof(description), stdin);
                description[strcspn(description, "\n")] = 0;
                credit(studentID, amount, description, bc);
                break;
                
            case 6:
                printf("enter student ID: ");
                scanf("%d", &studentID);
                printf("enter amount to pay: ");
                scanf("%f", &amount);
                printf("enter description: ");
                getchar();
                fgets(description, sizeof(description), stdin);
                description[strcspn(description, "\n")] = 0;
                pay(studentID, amount, description, bc);
                break;
                
            case 7:
                printf("enter source student ID: ");
                scanf("%d", &sourceID);
                printf("enter destination student ID: ");
                scanf("%d", &destID);
                printf("enter amount to transfer: ");
                scanf("%f", &amount);
                printf("enter description: ");
                getchar();
                fgets(description, sizeof(description), stdin);
                description[strcspn(description, "\n")] = 0;
                transfer(sourceID, destID, amount, description, bc);
                break;
                
            case 8:
                printf("enter filename to export: ");
                scanf("%s", filename);
                exportToFile(bc, filename);
                break;
                
            case 9:
                printf("enter filename to import: ");
                scanf("%s", filename);
                bc = importFromFile(filename);
                break;
                
            case 10:
                printf("thank you for using EATCoin!!!\n");
                break;
                
            default:
                printf("INVALID!!! please try again\n");
        }
        
    } while (choice != 10);
    
    freeBlockChain(bc);
    return 0;
}

//ayin tarixini bu gunu nece goturduyunu oyren
//doubly ya da circular linked list elave etseydik ne deyiserdi, etmeyi oyrenin
//butun funksiyalarin menasini, etc...

//gcc -o KAMRAN_NURAY main.c dsa_final_project.c 
//>> ./KAMRAN_NURAY