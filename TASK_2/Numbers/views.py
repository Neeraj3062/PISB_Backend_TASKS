from django.shortcuts import render
# from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request,'Numbers/home.html')



def print(request):
    if request.method == "POST" :

        data=int(request.POST["num"])
        if(data>0 and data<500):
            result= [i for i in range(1,data+1)]
            return render(request, 'Numbers/result.html', {"result":result})
    
        else:
            return render(request, 'Numbers/error.html')

    else:
        return render(request, 'Numbers/home.html' , )