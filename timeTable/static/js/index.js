document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("form");
  const submitBtn = document.getElementById("submitBtn");
  const clearBtn = document.getElementById("clearBtn");
  const departmentDropdown = document.getElementById("department");
  const staffNameDropdown = document.getElementById("staffName");
  const classNameDropdowm = document.getElementById("class");

  function updateDropdownOptions(
    sourceDropdown,
    targetDropdown,
    dataMapping,
    placeholderFunction,
    addSelectForAll = false
  ) {
    targetDropdown.innerHTML = "";

    if (addSelectForAll && targetDropdown.id === "class") {
      var selectOption = document.createElement("option");
      selectOption.value = "";
      selectOption.text = "Select";
      selectOption.selected = false;
      targetDropdown.add(selectOption);
    }

    if (sourceDropdown.value in dataMapping) {
      var sortedOptions = Array.from(dataMapping[sourceDropdown.value]).sort();

      if (sortedOptions.length === 0) {
        placeholderFunction(targetDropdown);
      }

      sortedOptions.forEach((optionValue) => {
        var option = document.createElement("option");
        option.value = optionValue;
        option.text = optionValue;
        targetDropdown.add(option);
      });
    } else {
      placeholderFunction(targetDropdown);
    }
  }

  function checkRequiredFields() {
    const requiredFields = form.querySelectorAll("[required]");
    const allFilled = [...requiredFields].every(
      (field) => field.value.trim() !== ""
    );

    submitBtn.disabled = !allFilled;
  }

  function updateStaffNames() {
    updateDropdownOptions(
      departmentDropdown,
      staffNameDropdown,
      departmentToStaff,
      addPlaceholderOption
    );
  }

  function updateClassNames() {
    updateDropdownOptions(
      departmentDropdown,
      classNameDropdowm,
      departmentToClassName,
      addPlaceholderOption,
      true
    );
  }

  function addPlaceholderOption(dropdown) {
    var placeholderOption = document.createElement("option");
    placeholderOption.value = "none";
    placeholderOption.text = "Select";
    placeholderOption.selected = true;
    placeholderOption.disabled = true;
    dropdown.add(placeholderOption);
  }

  form.addEventListener("input", function () {
    checkRequiredFields();
  });

  departmentDropdown.addEventListener("change", function () {
    updateStaffNames();
    updateClassNames();
    checkRequiredFields();
  });

  clearBtn.addEventListener("click", function () {
    form.reset();

    document
      .querySelectorAll(".formbold-form-label h3")
      .forEach(function (item) {
        item.innerHTML = "";
      });

    updateStaffNames();
    updateClassNames();
    checkRequiredFields();
  });

  updateStaffNames();
  updateClassNames();
  checkRequiredFields();
});
