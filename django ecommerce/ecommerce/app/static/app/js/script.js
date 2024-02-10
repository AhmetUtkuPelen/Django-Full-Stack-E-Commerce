// ! JQUERY JS FUNCTIONS ! \\



$('.plus-cart').click(function(){

    let id = $(this).attr("pid").toString()

    let eml = this.parentNode.children[2]

    $.ajax({

        type:"GET",
        url:"/pluscart",
        data:{
        prod_id:id
        },

        success:function(data){

            eml.innerText=data.quantity

            document.getElementById("amount").innerText=data.amount

            document.getElementById("totalamount").innerText=data.totalamount

        }

    })

})




$('.minus-cart').click(function(){

    let id = $(this).attr("pid").toString()

    let eml = this.parentNode.children[2]

    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
        prod_id:id
        },

        success:function(data){

            eml.innerText=data.quantity

            document.getElementById("amount").innerText=data.amount

            document.getElementById("totalamount").innerText=data.totalamount

        }

    })

})




$('.remove-cart').click(function(){

    let id = $(this).attr("pid").toString()

    let eml=this
    
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
    
        success:function(data){
    
            document.getElementById("amount").innerText=data.amount
    
            document.getElementById("totalamount").innerText=data.totalamount
    
            eml.parentNode.parentNode.parentNode.parentNode.remove()
    
        }

    })

})



$('.plus-wishlist').click(function(){

    let id = $(this).attr("pid").toString
    
    $.ajax({
        type:'GET',
        url:"/pluswishlist",
        data:{
            prod_id:id
        },
    
        success:function(data){
    
            window.location.href = `http://localhost:8000/product-detail/${id}`
    
        }

    })

})



$('.minus-wishlist').click(function(){
    
    let id = $(this).attr("pid").toString
    
    $.ajax({
        type:"GET",
        url:"/minuswishlist",
        data:{
            prod_id:id
        },
    
        success:function(data){
    
            window.location.href= `http://localhost:8000/product-detail/${id}`
    
        }

    })

})  

// !!! DARK MODE LIGHT MODE CONST !!! \\



const changecolor = document.getElementById('toggleDark')



const body = document.querySelector('body')





//  !DARK MODE LIGHT MODE CODE ! \\



changecolor.addEventListener('click', function(){

    this.classList.toggle('bi-moon')


    if(this.classList.toggle('bi-emoji-sunglasses')){

        body.style.background ='white'

    }else{

        body.style.background ='black'

    }

})

