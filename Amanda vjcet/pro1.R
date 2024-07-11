library(stringi)
palin<-function(x){
if(stri_reverse(x)==x){
 print(paste(x," is a palindrome"))
}else{
 			 print(paste(x," is not a palindrome"))
}
}

fact=function(y){
 		 factt=1
 		 if(y<0){
  			  print(paste(y, "is a negative number"))
 			 }else if(y==0) {
   		 print("The factorial of 0 is 1")
   		 palin(y)
  		}else{
   		 for (i in 1:y){
    		  factt=factt*i
    		}
   		 print(paste("The factorial of ", y," is ",factt ))
  		  palin(factt)
  		}
  
}
k=as.integer(readline("Enter a number: "))
fact(k)