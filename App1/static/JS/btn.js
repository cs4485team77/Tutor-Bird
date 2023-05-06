function searchfunction() {
  const table = document.getElementById("table");
  const tr = table.getElementsByTagName("tr");
  const search_filter = document.getElementById("search-filter").value.toUpperCase();

  // row
  for (var i = 0; i < tr.length; i++) {
    var td = tr[i].getElementsByTagName("td");
    // col
    for (var j = 0; j < td.length; j++) {
      // text
      var txt = td[j].innerText || td[j].textContent;
      if (search_filter === "") {
          tr[i].style.display = ""; //empty
          break;
      }
      else if (txt.toUpperCase().indexOf(search_filter) > -1) {
        tr[i].style.display = "";
        break;
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

document.getElementById("submit-button").addEventListener("click", function(event) {
  event.preventDefault();
  searchfunction();
});


/******************************************/


const favoriteButton = 'data-add-to-favorite';
const isFavorite = 'data-is-favorite';
const listSelector = '[data-my-favorites]';
class FavoritesList {
  constructor() {
    this.storageName = 'favoritesList';
    this.list = this.initList();
  }

  initList() {
    localStorage.clear();
    const list = JSON.parse(window.localStorage.getItem(this.storageName)) || [];
    this.updateHtmlList(list);
    return list;
  }

  initButton(button) {


    const name = button.getAttribute(favoriteButton);
    button.addEventListener('click', () => {
      const index = this.list.indexOf(name);
      if (index === -1) {
        this.list.push(name);
      } else {
        this.list.splice(index, 1);
      }
      this.setState(name);
      this.updateList();
    });

    this.setState(name);
    return button;
  }

  setState(name) {
    const button = document.querySelector(`[${favoriteButton}="${name}"]`);
    const redHeart = button.querySelector('#icon');
    const isFav = this.list.includes(name);
    if (isFav) {
      button.setAttribute(isFavorite, '');
      redHeart.style.color = 'red';
    } else {
      button.removeAttribute(isFavorite);
      redHeart.style.color = 'white';
    }

  }

  updateList() {
    window.localStorage.setItem(this.storageName, JSON.stringify(this.list));
    this.updateHtmlList(this.list);
  }

  updateHtmlList(list) {
    const favoritesHTMLElement = document.querySelector(listSelector);
    favoritesHTMLElement.innerHTML = '';
    if (list.length > 0) {
      const newList = [...list].reverse();
      newList.forEach((item) => {
        const htmlIcon = document.createElement('i');
        const htmlLi = document.createElement('li');

        htmlIcon.className = 'fa-solid fa-heart';
        htmlLi.style.padding = '15px';
        htmlLi.style.fontSize = '20px';
        htmlLi.style.listStyle = 'none';
        htmlIcon.style.color = 'red';
        htmlIcon.style.marginRight = '12px';
        htmlLi.appendChild(htmlIcon);
        htmlLi.appendChild(document.createTextNode(item));
        favoritesHTMLElement.appendChild(htmlLi);

      });
    }
  }
}

const buttons = document.querySelectorAll(`[${favoriteButton}]`);
const favorites = new FavoritesList();

buttons.forEach((button) => favorites.initButton(button));



/*****************************************/







