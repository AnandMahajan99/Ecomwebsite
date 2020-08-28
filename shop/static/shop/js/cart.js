  //find out the cart Items fron localStorage
  if(localStorage.getItem('cart') == null){
    var cart = {};
  }
  else{
    cart = JSON.parse(localStorage.getItem('cart'));
    updateCart(cart);
  }
  console.log(localStorage.getItem('cart'));
  //If the add to cart button is clicked, add/increment the item
  //  $('.cart').click(function(){
  $('.divpr').on('click','button.cart',function(){
    var idstr = this.id.toString();
<!--     if(cart[idstr] != undefined){-->
<!--       qty = cart[idstr][0] + 1;-->
<!--     }-->
console.log(idstr);
     if(cart[idstr] == undefined){
      qty = 1;
      name = document.getElementById('name' + idstr).innerHTML;
      img = $('#img' + idstr).attr('src');
      price = $('#price' + idstr).text();
<!--      $('#img').attr('src', img);-->
<!--      console.log(qty + name + img + price);-->
      cart[idstr] = [qty, name, img, price];
    }
    updateCart(cart);
    // localStorage.setItem('cart', JSON.stringify(cart));
    // document.getElementById('cart').innerHTML = Object.values(cart).length;
  });

  function updateCart(cart){
    sum = 0;
    i = 0;
    for(var item in cart){
      sum = sum + cart[item][0];
      i = i + 1;
      // document.getElementById('div'+ item ).innerHTML = "<button id='minus"+ item +"' class='btn btn-primary minus'> - </button><span id='val" + item +"'>" + cart[item][0] + "</span> <button id='plus" + item +"' class='btn btn-primary plus'> + </button>";
    }
    localStorage.setItem('cart', JSON.stringify(cart));

    document.getElementById('cart').innerHTML = i;
    //updateCartDropdown(cart);
  }

  //find out the cart Items fron localStorage
  if(localStorage.getItem('cart') == null){
    var cart = {};
  }
  else{
    cart = JSON.parse(localStorage.getItem('cart'));
    updateCart(cart);
  }
  console.log(localStorage.getItem('cart'));
  //If the add to cart button is clicked, add/increment the item
  //  $('.cart').click(function(){
  $('.divpr').on('click','button.cart',function(){
    var idstr = this.id.toString();
<!--     if(cart[idstr] != undefined){-->
<!--       qty = cart[idstr][0] + 1;-->
<!--     }-->
console.log(idstr);
     if(cart[idstr] == undefined){
      qty = 1;
      name = document.getElementById('name' + idstr).innerHTML;
      img = $('#img' + idstr).attr('src');
      price = $('#price' + idstr).text();
<!--      $('#img').attr('src', img);-->
<!--      console.log(qty + name + img + price);-->
      cart[idstr] = [qty, name, img, price];
    }
    updateCart(cart);
    // localStorage.setItem('cart', JSON.stringify(cart));
    // document.getElementById('cart').innerHTML = Object.values(cart).length;
  });

  function clearCart(){
    cart = JSON.parse(localStorage.getItem('cart'));
    for(var item in cart){
      document.getElementById('div' + item).innerHTML = '<button id="'+ item +'" class="btn btn-primary cart" style="margin-left:50px;">Add to Cart</button>';
    }
    localStorage.clear();
    cart = {};
    updateCart(cart);
  }

  function updateCart(cart){
    sum = 0;
    i = 0;
    for(var item in cart){
      sum = sum + cart[item][0];
      i = i + 1;
      // document.getElementById('div'+ item ).innerHTML = "<button id='minus"+ item +"' class='btn btn-primary minus'> - </button><span id='val" + item +"'>" + cart[item][0] + "</span> <button id='plus" + item +"' class='btn btn-primary plus'> + </button>";
    }
    localStorage.setItem('cart', JSON.stringify(cart));

    document.getElementById('cart').innerHTML = i;
    //updateCartDropdown(cart);
  }
