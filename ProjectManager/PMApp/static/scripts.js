// Wait till DOMCOntentLoaded
window.addEventListener("DOMContentLoaded", (event) => {

    // Script to automatically redirect when selected new project using projct selector
    document.querySelectorAll("[name=project_selector]")[0].addEventListener('change',
    function () {
        window.location = "/switch_project/" + this.value;
    });

    const editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(function(button) {
      button.addEventListener('click', function() {
        const type = button.dataset.type;   // 'task' or 'expense'
        const id = button.dataset.id;       // ID of the task/expense
        const staff = button.dataset.staff; // Staff type

        if (type === "task") {

          // Get the elements to toggle
          var save = document.getElementById("save-task-" + id);
          var deletebtn = document.getElementById("delete-task-" + id);
          var status = document.getElementById("status-" + id);
          var statusForm = document.getElementById("status-form-" + id);
          var priority = document.getElementById("priority-" + id);
          var priorityForm = document.getElementById("priority-form-" + id);
          var notes = document.getElementById("notes-" + id);
          var notesForm = document.getElementById("notes-form-" + id);
          var deadline = document.getElementById("deadline-" + id);
          var deadlineForm = document.getElementById("deadline-form-" + id);
          var members = document.getElementById("members-" + id);
          var membersForm = document.getElementById("members-form-" + id);

          // Get the current display value of each element
          var saveStyle = window.getComputedStyle(save).getPropertyValue("display");
          var statusStyle = window.getComputedStyle(status).getPropertyValue("display");
          var statusFormStyle = window.getComputedStyle(statusForm).getPropertyValue("display");
          if (staff == "M") {
            var deleteStyle = window.getComputedStyle(deletebtn).getPropertyValue("display");
            var priorityStyle = window.getComputedStyle(priority).getPropertyValue("display");
            var priorityFormStyle = window.getComputedStyle(priorityForm).getPropertyValue("display");
            var notesStyle = window.getComputedStyle(notes).getPropertyValue("display");
            var notesFormStyle = window.getComputedStyle(notesForm).getPropertyValue("display");
            var deadlineStyle = window.getComputedStyle(deadline).getPropertyValue("display");
            var deadlineFormStyle = window.getComputedStyle(deadlineForm).getPropertyValue("display");
            var membersStyle = window.getComputedStyle(members).getPropertyValue("display");
            var membersFormStyle = window.getComputedStyle(membersForm).getPropertyValue("display");
          }
          // Toggle the values
          button.innerHTML = button.innerHTML === "Edit" ? "Cancel" : "Edit";
          save.style.display = saveStyle === "none" || "" ? "inline-block" : "none";
          status.style.display = statusStyle === "none" || "" ? "inline-block" : "none";
          statusForm.style.display = statusFormStyle === "none" || "" ? "inline-block" : "none";
          if (staff == "M") {
            deletebtn.style.display = deleteStyle === "none" || "" ? "inline-block" : "none";
            priority.style.display = priorityStyle === "none" || "" ? "inline-block" : "none";
            priorityForm.style.display = priorityFormStyle === "none" || "" ? "inline-block" : "none";
            notes.style.display = notesStyle === "none" || "" ? "inline-block" : "none";
            notesForm.style.display = notesFormStyle === "none" || "" ? "inline-block" : "none";
            deadline.style.display = deadlineStyle === "none" || "" ? "inline-block" : "none";
            deadlineForm.style.display = deadlineFormStyle === "none" || "" ? "inline-block" : "none";
            members.style.display = membersStyle === "none" || "" ? "block" : "none";
            membersForm.style.display = membersFormStyle === "none" || "" ? "block" : "none";
          }


        } else {

          // Get the elements to toggle
          var save = document.getElementById("save-expense-" + id);
          var deletebtn = document.getElementById("delete-expense-" + id);
          var desc = document.getElementById("desc-" + id);
          var descForm = document.getElementById("desc-form-" + id);
          var amount = document.getElementById("amount-" + id);
          var amountForm = document.getElementById("amount-form-" + id);
          var date = document.getElementById("date-" + id);
          var dateForm = document.getElementById("date-form-" + id);

          // Get the current display value of each element
          var saveStyle = window.getComputedStyle(save).getPropertyValue("display");
          var deleteStyle = window.getComputedStyle(deletebtn).getPropertyValue("display");
          var descStyle  = window.getComputedStyle(desc).getPropertyValue("display");
          var descFormStyle  = window.getComputedStyle(descForm).getPropertyValue("display");
          var amountStyle  = window.getComputedStyle(amount).getPropertyValue("display");
          var amountFormStyle  = window.getComputedStyle(amountForm).getPropertyValue("display");
          var dateStyle  = window.getComputedStyle(date).getPropertyValue("display");
          var dateFormStyle  = window.getComputedStyle(dateForm).getPropertyValue("display");

          // Toggle the values
          button.innerHTML = button.innerHTML === "Edit" ? "Cancel" : "Edit";
          save.style.display = saveStyle === "none" || "" ? "inline-block" : "none";
          deletebtn.style.display = deleteStyle === "none" || "" ? "inline-block" : "none";
          desc.style.display = descStyle === "none" || "" ? "inline-block" : "none";
          descForm.style.display = descFormStyle === "none" || "" ? "inline-block" : "none";
          amount.style.display = amountStyle === "none" || "" ? "inline-block" : "none";
          amountForm.style.display = amountFormStyle === "none" || "" ? "inline-block" : "none";
          date.style.display = dateStyle === "none" || "" ? "inline-block" : "none";
          dateForm.style.display = dateFormStyle === "none" || "" ? "inline-block" : "none";
        }
      });
    });
});


// Toggle the div of the create form of the 'type',
// the div for the list of the 'oppositeType',
// and the button to create new 'type'
function toggleForm(type) {

    // Get the opposite type
    var oppositeType = (type === "tasks") ? "expenses" : "tasks";

    // Get the elements to toggle
    var divType = document.getElementById(type + "Form");
    var divOpposite = document.getElementById(oppositeType + "List");
    var btnType = document.getElementById(type + "CreateBtn");

    // Get the current display value of each element
    var divTypeCurrentStyle = window.getComputedStyle(divType).getPropertyValue("display");
    var divOppositeCurrentStyle = window.getComputedStyle(divOpposite).getPropertyValue("display");
    var btnTypeCurrentStyle = window.getComputedStyle(btnType).getPropertyValue("display");
    
    // Toggle the values
    divType.style.display = divTypeCurrentStyle === "none" || "" ? "block" : "none";
    divOpposite.style.display = divOppositeCurrentStyle === "none" ? "block" : "none";
    btnType.style.display = btnTypeCurrentStyle === "none" ? "inline-block" : "none";
}

