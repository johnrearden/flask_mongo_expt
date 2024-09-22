let currentSplitDiv = document.getElementById('split_div_1');
let currentSplitInput = currentSplitDiv.children[1];

currentSplitInput.addEventListener('change', () => {
    const splitID = parseInt(currentSplitInput.id.split('_')[1]);
    const newSplitDiv = currentSplitDiv.cloneNode(true);
    const newSplitInput = newSplitDiv.children[1];
    const newSplitLabel = newSplitDiv.children[0];

    newSplitInput.id = `split_${splitID + 1}`;
    newSplitInput.name = `split_${splitID + 1}`;
    newSplitInput.value = '';
    newSplitLabel.htmlFor = `split_${splitID + 1}`;
    newSplitLabel.innerText = `Split ${splitID + 1}`;
    document.getElementById('split_holder').appendChild(newSplitDiv);
    currentSplitDiv = newSplitDiv;
    currentSplitInput = newSplitInput;
    newSplitInput.focus();
});

currentSplitInput.addEventListener('keyup', (event) => {
    const value = event.target.value;
    const regex = /[^0-9:]/g
    event.target.value = event.target.value.replace(regex, '');
});