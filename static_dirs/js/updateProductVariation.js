// var updateBtnsCart = document.getElementsByClassName('update-price')
// var addToCartBtns = document.getElementsByClassName('prd-addto-cart')
var selColorBtns = document.getElementsByClassName('sel-color')
var selSizeBtns = document.getElementsByClassName('sel-size')
var color_id = ''
var size_id = ''

for(var i = 0; i < selColorBtns.length; i++){
  selColorBtns[i].addEventListener('click', function(){
    var productId = this.dataset.product
    var action = this.dataset.action
    color_id = this.dataset.value
    // document.getElementById("option-size").disabled = true;
    console.log(productId,action,color_id)
    // if(user == 'AnonymousUser'){
    //   // console.log('not loged in')
    //   addCookieItem(productId, action)
    //   updateGuessOrderCart(productId, action)
    // }else{
    //   updateProductImage(productId, color_id)
    // }
  })
}

for(var i = 0; i < selSizeBtns.length; i++){
  selSizeBtns[i].addEventListener('click', function(){
    var productId = this.dataset.product
    var action = this.dataset.action
    size_id = this.dataset.value
    console.log(productId,action,size_id)
    // if(user == 'AnonymousUser'){
    //   addCookieItem(productId, action)
    //   console.log('addtoCartGuessOrder', productId, action)
    //   addtoCartGuessOrder(productId, action)
    // }else{
    //   addtoCartUserOrder(productId, action)
    // }
  })
}


// function addCookieItem(productId, action){
//   console.log('not logged in..')
//
//   if(action == 'add'){
//     if(cart[productId] == undefined){
//       cart[productId] = {'quantity':1}
//     }else{
//       cart[productId]['quantity'] += 1
//     }
//   }
//
//   if(action == 'remove'){
//     cart[productId]['quantity'] -= 1
//
//     if(cart[productId]['quantity'] <= 0){
//       console.log('Remove')
//       delete cart[productId]
//     }
//   }
//   console.log('Cart:',cart)
//   document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
  // location.reload()
  // document.getElementById("cart-total").innerHTML = data['cartItems'];
  // document.getElementById("item-quantity-"+productId).innerHTML = data['orderItemQty'];
  // document.getElementById("item-total-"+productId).innerHTML = 'Rp  '+data['itemTotal'].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")+',-';
  // document.getElementById("items-total-qty").innerHTML = data['cartItems'];
  // document.getElementById("items-total-prc").innerHTML = 'Rp  '+data['cartTotal'].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")+',-';
// }


function updateUserOrderCart(productId, action, color_id, size_id){
  // console.log('User is logged in, sending data...')

  var url = '/update_variation/'

  var request = new Request(
    url,
    {headers: {'X-CSRFToken': csrftoken}}
  );

  fetch(url, {
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'X-CSRFToken': csrftoken
    },
    body:JSON.stringify({'productId': productId, 'action': action, 'color_id': color_id, 'size_id':size_id})
  })

  .then((response) =>{
    return response.json()
  })

  .then((data) =>{
    console.log('data:',data)
    // document.getElementById("cart-total").innerHTML = data['cartItems'];
    // document.getElementById("item-quantity-"+productId).innerHTML = data['orderItemQty'];
    // var $quant = $("#item-quantity-"+productId)
    // $quant.innerHTML = '';
    // $quant.fadeOut(1);
    // $quant.innerHTML = data['orderItemQty'];
    // $quant.fadeIn(300);
    // document.getElementById("item-total-"+productId).innerHTML = 'Rp  '+data['itemTotal'].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")+',-';
    // document.getElementById("items-total-qty").innerHTML = data['cartItems'];
    // document.getElementById("items-total-prc").innerHTML = 'Rp  '+data['cartTotal'].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")+',-';
    // location.reload()
  })

}
//
//
// function updateGuessOrderCart(productId, action){
//
//   var url = '/update_item/'
//
//   fetch(url, {
//     method:'POST',
//     headers:{
//       'Content-Type':'application/json',
//       'X-CSRFToken': csrftoken
//     },
//     body:JSON.stringify({'productId': productId, 'action': action})
//   })
//
//   .then((response) =>{
//     return response.json()
//   })
//
//   .then((data) =>{
//     exist = false
//     for(i=0; i < data.items.length; i++){
//       if(data.items[i].product.id == productId) {
//         exist = true
//       }
//     }
//     if(exist == false){
//       document.getElementById("item-row-"+productId).classList.add('hidden');
//     }
//     if(data.items.length != 0){
//       for(i=0; i < data.items.length; i++){
//         if(data.items[i].product.id == productId){
//             var $quant = $("#item-quantity-"+productId)
//             $quant.innerHTML = '';
//             $quant.fadeOut(1);
//             $quant.innerHTML = data.items[i].quantity;
//             $quant.fadeIn(300);
//             document.getElementById("item-quantity-"+productId).innerHTML = data.items[i].quantity;
//             document.getElementById("item-total-"+productId).innerHTML = 'Rp  '+data.items[i].get_total.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")+',-';
//         }
//         document.getElementById("cart-total").innerHTML = data['cart_total'];
//         document.getElementById("items-total-qty").innerHTML = data['cart_total'];
//         document.getElementById("items-total-prc").innerHTML = 'Rp  '+data['grand_total'].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")+',-';
//       }
//     }else{
//       document.getElementById("cart-total").innerHTML = data['cart_total'];
//       document.getElementById("items-total-qty").innerHTML = '0';
//       document.getElementById("items-total-prc").innerHTML = 'Rp  0,-';
//       document.getElementById("checkout-btn").classList.add('hidden');
//     }
//   })
//
// }
//
//
// function addtoCartUserOrder(productId, action){
//   // console.log('User is logged in, sending data...')
//
//   var url = '/update_item/'
//
//   // var request = new Request(
//   //   url,
//   //   {headers: {'X-CSRFToken': csrftoken}}
//   // );
//
//   fetch(url, {
//     method:'POST',
//     headers:{
//       'Content-Type':'application/json',
//       'X-CSRFToken': csrftoken
//     },
//     body:JSON.stringify({'productId': productId, 'action': action})
//   })
//
//   .then((response) =>{
//     return response.json()
//   })
//
//   .then((data) =>{
//     // console.log('data:',data)
//     document.getElementById("cart-total").innerHTML = data['cartItems'];
//     // document.getElementById("item-quantity-"+productId).innerHTML = data['orderItemQty'];
//     // location.reload()
//   })
//
// }
//
//
// function addtoCartGuessOrder(productId, action){
//   console.log('User is logged in, sending data...')
//
//   var url = '/update_item/'
//
//   // var request = new Request(
//   //   url,
//   //   {headers: {'X-CSRFToken': csrftoken}}
//   // );
//
//   fetch(url, {
//     method:'POST',
//     headers:{
//       'Content-Type':'application/json',
//       'X-CSRFToken': csrftoken
//     },
//     body:JSON.stringify({'productId': productId, 'action': action})
//   })
//
//   .then((response) =>{
//     return response.json()
//   })
//
//   .then((data) =>{
//     console.log('data:',data)
//     document.getElementById("cart-total").innerHTML = data['cart_total'];
//     // document.getElementById("item-quantity-"+productId).innerHTML = data['orderItemQty'];
//     // location.reload()
//   })
//
// }
