const titleInput = document.getElementById("id_title");
const titleCount = document.getElementById("title-count");
const tagSelect = document.getElementById("id_tags");
const tagButtons = document.getElementById("tag-buttons");
const tagOptions = tagSelect.querySelectorAll("option");
const bodyInput = document.getElementById("id_body");
const markdownPreview = document.getElementById("markdown-preview");

function updateTitleCount() {
    const count = titleInput.value.length;

    titleCount.textContent = `${count} / 50文字`;

    if (count > 50) {
        titleCount.textContent += " ※50文字以内で入力してください";
    }
}

titleInput.addEventListener("input", updateTitleCount);

updateTitleCount();


tagOptions.forEach(function (option) {
    const button = document.createElement("button");

    button.type = "button";
    button.textContent = option.textContent;

    // ★ 編集画面を開いた時点ですでに選択済みなら ✓ をつける
    if (option.selected) {
        button.textContent = `✓ ${option.textContent}`;
    }

    button.addEventListener("click", function () {
        option.selected = !option.selected;

        if (option.selected) {
            button.textContent = `✓ ${option.textContent}`;
        } else {
            button.textContent = option.textContent;
        }
    });

    tagButtons.appendChild(button);
});

tagSelect.style.display = "none";


function updateMarkdownPreview() {
    const markdownHtml = marked.parse(bodyInput.value);
    const safeHtml = DOMPurify.sanitize(markdownHtml);

    markdownPreview.innerHTML = safeHtml;
}

bodyInput.addEventListener("input", updateMarkdownPreview);

updateMarkdownPreview();