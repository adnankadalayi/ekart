
// cart item increment ajax
$('.plus_cart').on('click', function () {
    var id = $(this).attr('pid').toString();
    console.log(id)
    $ajax({
        type: 'GET',
        url: '/plus_cart',
        data: {
            prod_id: id
        },
        success: function (data) {
            console.log(data)
            console.log('success')
        }
    })
});

// Activate selected address
$(document).on('click','.activate-address',function(){
    var _aId=$(this).attr('data-address');
    var _vm=$(this);
    // Ajax
    $.ajax({
        url:'/activate-address',
        data:{
            'id':_aId,
        },
        dataType:'json',
        success:function(res){
            console.log(res);
            if(res.bool==true){
                $(".address").removeClass('shadow border-secondary');
                $(".address"+_aId).addClass('shadow border-secondary');

                $(".check").hide();
                $(".actbtn").show();
                
                $(".check"+_aId).show();
                $(".btn"+_aId).hide();
            }
        }
    });
    // End
});

// // add to cart ajax
// $('.addToCart').click(function (e) {
//     e.preventDefault();

// });

// Add to cart
	// $(document).on('click',"#addToCartBtn",function(){
	// 	var _vm=$(this);
	// 	var _index=_vm.attr('data-index');
	// 	var _qty=$(".product-qty-"+_index).val();
	// 	var _productId=$(".product-id-"+_index).val();
	// 	var _productImage=$(".product-image-"+_index).val();
	// 	var _productTitle=$(".product-title-"+_index).val();
	// 	var _productPrice=$(".product-price-"+_index).text();
	// 	// Ajax
	// 	$.ajax({
	// 		url:'/add-to-cart',
	// 		data:{
	// 			'id':_productId,
	// 			'image':_productImage,
	// 			'qty':_qty,
	// 			'title':_productTitle,
	// 			'price':_productPrice
	// 		},
	// 		dataType:'json',
	// 		beforeSend:function(){
	// 			_vm.attr('disabled',true);
	// 		},
	// 		success:function(res){
	// 			$(".cart-list").text(res.totalitems);
	// 			_vm.attr('disabled',false);
	// 		}
	// 	});
	// 	// End
	// });
	// // End
