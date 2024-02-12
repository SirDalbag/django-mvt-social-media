const searchInput = document.getElementById('search');
const clearButton = document.getElementById('clear');
const focusIcons = document.querySelectorAll('#icon');
const contentInput = document.getElementById('content');
const imageInput = document.getElementById('image');
const postButton = document.getElementById('post');

function updatePostButtonState() {
    postButton.disabled = !contentInput.value.trim().replace(/\s/g, '') && imageInput.files.length === 0;
}

if (contentInput) {
    contentInput.addEventListener('input', updatePostButtonState);
}

if (clearButton) {
    clearButton.addEventListener('click', function () {
        searchInput.value = '';
        clearButton.classList.add('hidden');
    });
}

if (imageInput) {
    imageInput.addEventListener('change', updatePostButtonState);
}

if (searchInput) {
    searchInput.addEventListener('input', function () {
        clearButton.classList.toggle('hidden', !searchInput.value);
    });
}

focusIcons.forEach((focusIcon) => {
    searchInput.addEventListener('focus', function () {
        focusIcon.classList.add('stroke-sky-500');
    });

    searchInput.addEventListener('blur', function () {
        focusIcon.classList.remove('stroke-sky-500');
    });
});

function displayImage(input) {
    let imageContainer = document.getElementById('container');
    if (input.files && input.files[0]) {
        let reader = new FileReader();
        reader.onload = function (e) {
            let imageContainerItem = document.createElement('div');
            let uniqueId = Date.now();
            imageContainerItem.id = `imageItem_${uniqueId}`;
            imageContainerItem.className = 'z-10 w-full sm:w-1/2 md:w-1/2 lg:w-1/2 xl:w-1/2';
            imageContainerItem.innerHTML = `
                <div class="relative h-[125px] w-[125px] lg:h-[250px] lg:w-[250px]">
                    <img src="${e.target.result}" class="h-[125px] w-[125px] lg:h-[250px] lg:w-[250px] rounded-lg p-3">
                    <button type="button" onclick="removeImage(${uniqueId})" class="absolute right-4 top-4 lg:right-5 lg:top-5 rounded-full bg-zinc-900 bg-opacity-65 bg-blur backdrop-filter backdrop-blur-lg hover:bg-opacity-80">
                        <svg id="icon" class="w-6 h-6 p-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                    </button>
                </div>
            `;
            imageContainer.appendChild(imageContainerItem);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function removeImage(uniqueId) {
    let imageContainerItem = document.getElementById(`imageItem_${uniqueId}`);
    if (imageContainerItem) {
        imageContainerItem.remove();
        imageInput.value = '';
        updatePostButtonState();
    }
}

function previewImage(event) {
    let inputElement = event.target;
    let files = inputElement.files;
    if (files.length > 0) {
        let previewImageElement = document.getElementById('preview');
        let reader = new FileReader();
        reader.onload = function (e) {
            previewImageElement.src = e.target.result;
        };
        reader.readAsDataURL(files[0]);
    }
}