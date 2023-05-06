const cells = document.querySelectorAll('td.cell');
const button = document.getElementById('submitBtn');
const form = document.getElementById("form_1")
let highlightedCells = [];
const highlightedInput = document.getElementById('highlighted-cells');
const row = document.getElementById("highlighted-row");
const column = document.getElementById("highlighted-column");
let rowl = [];
let columnl = [];

cells.forEach(cell => {
  cell.addEventListener('click', function() {
    // Toggle the background color
    if (this.style.backgroundColor === 'lightgreen') {
      this.style.backgroundColor = '';
      let rowIndex = this.parentElement.rowIndex - 1; // Subtract 1 to account for the header row
      let cellIndex = this.cellIndex - 1; // Subtract 1 to account for the first column being the time slot
      highlightedCells = highlightedCells.filter(item => item !== this.innerText);
      rowl = rowl.filter(item => item !== rowIndex);
      columnl = columnl.filter(item => item !== cellIndex);
    } else {
      this.style.backgroundColor = 'lightgreen';
      highlightedCells.push(this.innerText);
      // Find the row and column index of the highlighted cell
      let rowIndex = this.parentElement.rowIndex - 1; // Subtract 1 to account for the header row
      let cellIndex = this.cellIndex - 1; // Subtract 1 to account for the first column being the time slot

      rowl.push(rowIndex);
      columnl.push(cellIndex);

      console.log("Highlighted cell: row = " + rowIndex + ", column = " + cellIndex);
    }

    row.setAttribute('value', rowl.join(','));
    column.setAttribute('value', columnl.join(','));
    highlightedInput.setAttribute('value', highlightedCells.join(','));
  });
});
