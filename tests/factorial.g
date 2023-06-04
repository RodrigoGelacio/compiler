program lol;

func int fact(int num){
    int i;
    if(num == 1){
        return (1);
    }

    return (num * fact(num-1));
}

main(){

    int i;

    i = fact(5);

    print(i);

}