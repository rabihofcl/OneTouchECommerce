
console.log('Hello World')
const alertBox = document.getElementById('alert-box')
const imageBox = document.getElementById('image-box')
const imageForm = document.getElementById('image-form')
console.log(imageForm)
const confirmBtn = document.getElementById('confirm-btn')
const input = document.getElementById('id_logo')

const csrf = document.getElementsByName('csrfmiddlewaretoken')


input.addEventListener('change', ()=>{
    console.log('changed')

    const img_data = input.files[0]
    const url = URL.createObjectURL(img_data)
    imageBox.innerHTML = '<img src="${url}" id="image" width="500px"'

    var $image = $('#image');

    $image.cropper({
    aspectRatio: 16 / 9,
        crop: function(event) {
            console.log(event.detail.x);
            console.log(event.detail.y);
            console.log(event.detail.width);
            console.log(event.detail.height);
            console.log(event.detail.rotate);
            console.log(event.detail.scaleX);
            console.log(event.detail.scaleY);
        }
        });

})