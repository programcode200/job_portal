// const editor = document.getElementById('editor');
// const boldButton = document.getElementById('bold');
// const italicButton = document.getElementById('italic');
// const unorderedListButton = document.getElementById('unorderedList');

// boldButton.addEventListener('click', (e) => {
//     e.preventDefault(); // Prevent the default behavior of the button
//     applyFormatting('bold');
// });

// italicButton.addEventListener('click', (e) => {
//     e.preventDefault(); // Prevent the default behavior of the button
//     applyFormatting('italic');
// });

// unorderedListButton.addEventListener('click', (e) => {
//     e.preventDefault(); // Prevent the default behavior of the button
//     applyFormatting('insertUnorderedList');
// });

// function applyFormatting(format) {
//     const selection = window.getSelection();
//     const range = selection.getRangeAt(0);

//     if (format === 'bold') {
//         document.execCommand('bold');
//     } else if (format === 'italic') {
//         document.execCommand('italic');
//     } else if (format === 'insertUnorderedList') {
//         document.execCommand('insertUnorderedList');
//     }
// }


document.addEventListener('DOMContentLoaded', function() {
    const editor = document.getElementById('editor');
    const boldButton = document.getElementById('bold');
    const italicButton = document.getElementById('italic');
    const unorderedListButton = document.getElementById('unorderedList');

    boldButton.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent the default behavior of the button
        applyFormatting('bold');
    });

    italicButton.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent the default behavior of the button
        applyFormatting('italic');
    });

    unorderedListButton.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent the default behavior of the button
        applyFormatting('insertUnorderedList');
    });

    function applyFormatting(format) {
        const selection = window.getSelection();
        const range = selection.getRangeAt(0);

        if (format === 'bold') {
            document.execCommand('bold');
        } else if (format === 'italic') {
            document.execCommand('italic');
        } else if (format === 'insertUnorderedList') {
            document.execCommand('insertUnorderedList');
        }
    }
});




