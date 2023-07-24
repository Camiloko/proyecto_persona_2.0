 // Código JavaScript para generar el gráfico de Gantt

 let tasks = [];
 let ganttContainer;
 let gantt;

 // Variable para almacenar la tarea seleccionada al hacer clic
 let selectedTask = null;

 function agregarTarea() {
     let taskName = document.getElementById("taskName").value;
     let startDate = document.getElementById("startDate").value;
     let endDate = document.getElementById("endDate").value;

     if (taskName && startDate && endDate) {
         tasks.push({
             id: 'Task ' + (tasks.length + 1),
             name: taskName,
             start: startDate,
             end: endDate,
             progress: 0,
         });

         document.getElementById("taskName").value = "";
         document.getElementById("startDate").value = "";
         document.getElementById("endDate").value = "";

         dibujarGantt();
     } else {
         alert("Por favor, completa todos los campos.");
     }
 }

 function dibujarGantt() {
     ganttContainer = document.getElementById("ganttChart");
     ganttContainer.innerHTML = "";

     gantt = new Gantt("#ganttChart", tasks, {
         on_click: function(task) {
             if (task) {
                 // Guardar la tarea seleccionada
                 selectedTask = task;
                 // Mostrar el selector de color
                 document.getElementById("colorSelector").click();
             }
         },
     });
 }

 // Evento para cambiar el color de la barra al seleccionar un color en el selector
 document.getElementById("colorSelector").addEventListener("input", function() {
     if (selectedTask) {
         // Obtener el color seleccionado y aplicarlo a la barra
         let color = this.value;
         let bar = gantt.get_bar(selectedTask.id);
         if (bar) {
             bar.$bar.style.fill = color;
         }
         // Reiniciar la tarea seleccionada
         selectedTask = null;
     }
 });