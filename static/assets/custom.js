$('.addQuantity').click(function (e){
    e.preventDefault();
    var product_id = $(this).closest('.product_data').find('.prod_id').val();
    // var product_qty = $(this).closest('.product_data').find('.qty-input').val();
    var token  = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        method : 'POST',
        url : '/cart/add-cart',
        data :{
            'product_id': product_id,
            // 'product_qty': product_qty,
            csrfmiddlewaretoken : token
        },
        success : function (response) {
            alert.success(response.status)
            alertify.success(response.status)
        }
    });
});
$('.lessQuantity').click(function (e){
    e.preventDefault();
    var product_id = $(this).closest('.product_data').find('.prod_id').val();
    // var product_qty = $(this).closest('.product_data').find('.qty-input').val();
    var token  = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        method : 'POST',
        url : '/cart/less-cart',
        data :{
            'product_id': product_id,
            // 'product_qty': product_qty,
            csrfmiddlewaretoken : token
        },
        success : function (response) {
            alert.success(response.status)
            alertify.success(response.status)
        }
    });
});
