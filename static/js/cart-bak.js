var updateBtnsCart = document.getElementsByClassName('update-cart')
var addToCartBtns = document.getElementsByClassName('addto-cart')

for(var i = 0; i < updateBtnsCart.length; i++){
  updateBtnsCart[i].addEventListener('click', function(){
    var productId = this.dataset.product
    var action = this.dataset.action
    if(user == 'AnonymousUser'){
      addCookieItem(productId, action)
      updateUserOrderCart(productId, action)
    }else{
      updateUserOrderCart(productId, action)
    }
  })
}

for(var i = 0; i < addToCartBtns.length; i++){
  addToCartBtns[i].addEventListener('click', function(){
    var productId = this.dataset.product
    var action = this.dataset.action
    if(user == 'AnonymousUser'){
      addCookieItem(productId, action)
      addtoCartUserOrder(productId, action)
    }else{
      addtoCartUserOrder(productId, action)
    }
  })
}


function addCookieItem(productId, action){
  console.log('not logged in..')

  if(action == 'add'){
    if(cart[productId] == undefined){
      cart[productId] = {'quantity':1}
    }else{
      cart[productId]['quantity'] += 1
    }
  }

  if(action == 'remove'){
    cart[productId]['quantity'] -= 1

    if(cart[productId]['quantity'] <= 0){
      console.log('Remove')
      delete cart[productId]
    }
  }
  console.log('Cart:',cart)
  document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
}


function updateUserOrderCart(productId, action){

  var url = '/update_item/'

  fetch(url, {
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'X-CSRFToken': csrftoken
    },
    body:JSON.stringify({'productId': productId, 'action': action})
  })

  .then((response) =>{
    return response.json()
  })

  .then((data) =>{
    exist = false
    for(i=0; i < data.items.length; i++){
      if(data.items[i].product.id == productId) {
        exist = true
      }
    }
    if(exist == false){
      document.getElementById("item-row-"+productId).classList.add('hidden');
    }
    if(data.items.length != 0){
      for(i=0; i < data.items.length; i++){
        if(data.items[i].product.id == productId){
            document.getElementById("item-quantity-"+productId).innerHTML = data.items[i].quantity;
            document.getElementById("item-total-"+productId).innerHTML = 'Rp. '+data.items[i].get_total.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")+',-';
        }
        document.getElementById("cart-total").innerHTML = data['cart_total'];
        document.getElementById("items-total-qty").innerHTML = data['cart_total'];
        document.getElementById("items-total-prc").innerHTML = 'Rp. '+data['grand_total'].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")+',-';
      }
    }else{
      document.getElementById("cart-total").innerHTML = data['cart_total'];
      document.getElementById("items-total-qty").innerHTML = '0';
      document.getElementById("items-total-prc").innerHTML = 'Rp. 0,-';
      document.getElementById("checkout-btn").classList.add('hidden');
    }
  })

}

function addtoCartUserOrder(productId, action){

  var url = '/update_item/'

  fetch(url, {
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'X-CSRFToken': csrftoken
    },
    body:JSON.stringify({'productId': productId, 'action': action})
  })

  .then((response) =>{
    return response.json()
  })

  .then((data) =>{
    // console.log(data)
    document.getElementById("cart-total").innerHTML = data['cart_total'];
  })

}
