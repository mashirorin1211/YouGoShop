let first_select = document.getElementById('firstcategory');
let second_select = document.getElementById('secondcategory');

function get_second_selection() {
    first_id = first_select.value;
    fetch('/category/'+first_id).then((response)=>{
        response.json().then((data)=>{
            let optionHTML = '';
            for (let second of data.seconds) {
                optionHTML += '<option value="' + second.id +'">' + second.title + '</option>';
            }
            second_select.innerHTML = optionHTML;
        })
    });
}

window.onload = () => {
    get_second_selection();
    first_select.onchange = () => {
        get_second_selection();
    }
    $('.select-search').select2({
        width: '100%'
    });
}