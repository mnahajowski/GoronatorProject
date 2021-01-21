function verification() {
    // send to verification
    document.getElementById('verification-icon').setAttribute('src', '/static/images/share-icon-grey.svg')
    document.getElementById('verification-icon').style.cursor = 'default'
    document.getElementById('verification-icon').onclick = () => false
}