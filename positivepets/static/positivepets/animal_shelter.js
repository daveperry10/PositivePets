/* client-side functions to populate html select elements for animal shelter page */


function loadMe(animal_array, breed_dict){

    var animalSelect = this.document.getElementById("animal_type");

    var animal = localStorage.getItem("animalSelect")
    //alert(animal)

    for (var i=0; i<animal_array.length; i++){
        var option = this.document.createElement("option");
        option.text = animal_array[i];
        animalSelect.add(option)
    }
    if (animal != null){
        animalSelect.value = animal;
    }
    fillBreeds(breed_dict);


    //animalSelect.innerHTML="";  // clean out the select list


}

function fillBreedsJson(jsonObject){
    var breed_dict = JSON.parse(jsonObject)
    fillBreeds(breed_dict)
}

function fillBreeds(breed_dict){
    //var jsonObject = JSON.parse('str);

    // get the selected animal
    var select_element = document.getElementById("animal_type");
    var animal;
    for (var i=0; i<select_element.length; i++){
        if (select_element.children[i].selected === true){
            animal = select_element.children[i].value;
            }
    }

    // get the correct array out of the dictionary
    var breed_array = breed_dict[animal]

    // populate the select element
    var breedSelect = document.getElementById("breed")
    breedSelect.innerHTML="";
    for (var i=0; i<breed_array.length; i++){
        var option = document.createElement("option");
        option.text = breed_array [i];
        breedSelect.add(option)
    }

    breed = localStorage.getItem("breedSelect")
    if (breed != null){
        breedSelect.value = localStorage.getItem("breedSelect")
    }

    searchWords = localStorage.getItem("searchWordsSelect")
    var searchWordsSelect = document.getElementById("search_words")
    if (searchWords != null){
        searchWordsSelect.value = searchWords
    }

}

function makeBig(img_url){
    //alert("make it big")
}

function saveState(){
    var animalSelect = document.getElementById("animal_type")
    localStorage.setItem("animalSelect",animalSelect.value)

    var breedSelect = document.getElementById("breed")
    localStorage.setItem("breedSelect",breedSelect.value)

    var searchWordsSelect = document.getElementById("search_words")
    localStorage.setItem("searchWordsSelect",searchWordsSelect.value)
    }