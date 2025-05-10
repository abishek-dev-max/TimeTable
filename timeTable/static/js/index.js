document.addEventListener("DOMContentLoaded", () => {
  // Get references to DOM elements once, to avoid repeated lookups
  const form = document.getElementById("form");
  const submitBtn = document.getElementById("submitBtn");
  const clearBtn = document.getElementById("clearBtn");
  const departmentDropdown = document.getElementById("department");
  const staffNameDropdown = document.getElementById("staffName");
  const classNameDropdown = document.getElementById("class");
  const labelHeaders = document.querySelectorAll(".formbold-form-label h3");

  // Utility function to create <option> elements with optional attributes
  const createOption = (
    value,
    text,
    { selected = false, disabled = false } = {}
  ) => {
    const option = document.createElement("option");
    option.value = value;
    option.text = text;
    if (selected) option.selected = true;
    if (disabled) option.disabled = true;
    return option;
  };

  // Function to update dropdown options based on source dropdown selection and mapping data
  const updateDropdownOptions = (
    sourceDropdown,
    targetDropdown,
    dataMapping
  ) => {
    const options = [];

    // Add default "Select" option for specific dropdowns
    if (["class", "staffName"].includes(targetDropdown.id)) {
      options.push(createOption("", "Select"));
    }

    // Fetch mapped values from the selected source and sort them
    const values = dataMapping[sourceDropdown.value] || [];
    if (values.length) {
      values
        .sort()
        .forEach((value) => options.push(createOption(value, value)));
    } else {
      // Add placeholder if no valid values exist
      options.push(
        createOption("none", "Select", { selected: true, disabled: true })
      );
    }

    // Replace all children at once to minimize reflow and improve performance
    targetDropdown.replaceChildren(...options);
  };

  // Function to validate that all required fields in the form are filled
  const checkRequiredFields = () => {
    const allFilled = Array.from(form.querySelectorAll("[required]")).every(
      (field) => field.value.trim() !== ""
    );
    submitBtn.disabled = !allFilled;
  };

  // Convenience function to update both dependent dropdowns based on the selected department
  const updateFormDropdowns = () => {
    updateDropdownOptions(
      departmentDropdown,
      staffNameDropdown,
      departmentToStaff
    );
    updateDropdownOptions(
      departmentDropdown,
      classNameDropdown,
      departmentToClassName
    );
  };

  // Add event listener for form inputs to validate required fields dynamically
  form.addEventListener("input", checkRequiredFields);

  // Update dependent dropdowns and check field validity when department changes
  departmentDropdown.addEventListener("change", () => {
    updateFormDropdowns();
    checkRequiredFields();
  });

  // Reset form, labels, and dropdowns when clear button is clicked
  clearBtn.addEventListener("click", () => {
    form.reset();
    labelHeaders.forEach((header) => (header.innerHTML = ""));
    updateFormDropdowns();
    checkRequiredFields();
  });

  // Initial setup: populate dropdowns and validate required fields
  updateFormDropdowns();
  checkRequiredFields();
});
