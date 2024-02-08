document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("form");
  const submitBtn = document.getElementById("submitBtn");
  const clearBtn = document.getElementById("clearBtn");
  const departmentDropdown = document.getElementById("department");
  const staffNameDropdown = document.getElementById("staffName");

  function checkRequiredFields() {
    const requiredFields = form.querySelectorAll("[required]");
    const allFilled = [...requiredFields].every(
      (field) => field.value.trim() !== ""
    );

    submitBtn.disabled = !allFilled;
  }

  function updateStaffNames() {
    staffNameDropdown.innerHTML = "";

    var selectedDepartment = departmentDropdown.value;
    var departmentToStaffMap = departmentToStaff;

    if (selectedDepartment in departmentToStaffMap) {
      var uniqueStaffNames = new Set(departmentToStaffMap[selectedDepartment]);
      var sortedStaffNames = Array.from(uniqueStaffNames).sort();

      if (sortedStaffNames.length === 0) {
        addPlaceholderOption();
      }

      sortedStaffNames.forEach((staffName) => {
        var option = document.createElement("option");
        option.value = staffName;
        option.text = staffName;
        staffNameDropdown.add(option);
      });
    } else {
      addPlaceholderOption();
    }
  }

  function addPlaceholderOption() {
    var placeholderOption = document.createElement("option");
    placeholderOption.value = "none";
    placeholderOption.text = "Select a staff";
    placeholderOption.selected = true;
    placeholderOption.disabled = true;
    staffNameDropdown.add(placeholderOption);
  }
  form.addEventListener("input", function () {
    checkRequiredFields();
  });

  departmentDropdown.addEventListener("change", function () {
    updateStaffNames();
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

    checkRequiredFields();
  });

  updateStaffNames();
  checkRequiredFields();
});
