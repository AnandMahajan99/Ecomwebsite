
    console.log("hello");   // for checking

    cart = JSON.parse(localStorage.getItem('cart'));
    updateCart(cart);

  function updateCart(cart){
    i = 0;
    for(var item in cart){
      i = i + 1;
    }
//    localStorage.setItem('cart', JSON.stringify(cart));

    document.getElementById('cart').innerHTML = i;
  }
