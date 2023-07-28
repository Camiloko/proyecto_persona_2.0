let ganttContainer;
let gantt;

let selectedTask = null;
let tasks = [];
let hasTasks = false; 

function cargarDiagrama() {
    $.ajax({
        type: "GET",
        url: "/get_user_tasks", 
        dataType: "json",
        success: function(data) {
            if (data.tasks && data.tasks.length > 0) {
                tasks = data.tasks.map((task, index) => {
                    return {
                        name: task.tarea,
                        dbID: task.id,
                        start: moment(task.fecha_inicio).format("YYYY-MM-DD"), 
                        end: moment(task.fecha_termino).format("YYYY-MM-DD"), 
                    };
                });
                hasTasks = true;
                dibujarGantt(); 
            } else {
                hasTasks = false;
                let ganttContainer = document.getElementById("ganttChart");
                ganttContainer.innerHTML = "<p>No hay tareas disponibles.</p>";
            }
            let taskSelect = document.getElementById("taskSelect");
            taskSelect.innerHTML = ""; 
            tasks.forEach((task) => {
                let option = document.createElement("option");
                option.value = task.dbID; 
                option.textContent = task.name; 
                taskSelect.appendChild(option);
            });
        },
        error: function() {
            alert("No tienes tareas creadas.");
        }
    });
}

// Función para agregar una nueva tarea con un color predeterminado
function dibujarYGuardarTarea() {
    let taskName = document.getElementById("taskName").value;
    let startDateString = document.getElementById("startDate").value;
    let endDateString = document.getElementById("endDate").value;

    if (taskName && startDateString && endDateString) {
        if (!hasTasks) {
            tasks = []; 
        }
        let color = document.getElementById("colorSelector").value;

        let startDate = new Date(startDateString);
        let endDate = new Date(endDateString);

        startDate.setUTCHours(0, 0, 0, 0);
        endDate.setUTCHours(0, 0, 0, 0);

        let startDateStringUTC = startDate.toISOString().split('T')[0];
        let endDateStringUTC = endDate.toISOString().split('T')[0];

        tasks.push({
            id: 'Task ' + (tasks.length + 1),
            name: taskName,
            start: startDateStringUTC,
            end: endDateStringUTC,
            custom_class: `custom_class_${tasks.length + 1}_${color}` 
        });

        document.getElementById("taskName").value = "";
        document.getElementById("startDate").value = "";
        document.getElementById("endDate").value = "";

        dibujarGantt();
        guardarTarea();
        hasTasks = true; 
    } else {
        alert("Por favor, completa todos los campos.");
    }
}




///////////////////////////////

         function eliminarTarea(taskId) {
            if (confirm("¿Estás seguro que deseas eliminar esta tarea?")) {
                let data = {
                    "id": taskId
                };
       
                $.ajax({
                    type: "POST",
                    url: "/eliminar_tarea",
                    data: JSON.stringify(data),
                    contentType: "application/json",
                    dataType: "json",
                    success: function(response) {
                        if (response.message) {
                            console.log("Tarea eliminada:", response.message);
                            cargarDiagrama();
                        } else {
                            console.error("Error al eliminar la tarea:", response.error);
                        }
                        
                    },
                    error: function(error) {
                        console.error("Error al realizar la solicitud:", error);
                    }
                });
            }
        }


function dibujarGantt() {
    ganttContainer = document.getElementById("ganttChart");
    ganttContainer.innerHTML = "";

    gantt = new Gantt("#ganttChart", tasks, {
        language: "es",
        on_click: function(task) {
            if (task) {
                selectedTask = task;
                document.getElementById("colorSelector").click();
            }
        },
        on_date_change: function(task, start, end) {
            let taskName = task.name;
            let startDate = new Date(start);
            let endDate = new Date(end);

            let startYear = startDate.getFullYear();
            let startMonth = String(startDate.getMonth() + 1).padStart(2, '0');
            let startDay = String(startDate.getDate()).padStart(2, '0');

            let endYear = endDate.getFullYear();
            let endMonth = String(endDate.getMonth() + 1).padStart(2, '0');
            let endDay = String(endDate.getDate()).padStart(2, '0');

            let startDateString = `${startYear}-${startMonth}-${startDay}`;
            let endDateString = `${endYear}-${endMonth}-${endDay}`;

            let data = {
                "name": taskName,
                "start": startDateString,
                "end": endDateString
            };

            $.ajax({
                type: "POST",
                url: "/actualizar_tarea",
                data: JSON.stringify(data),
                contentType: "application/json",
                dataType: "json",
                success: function(data) {
                    if (data.message) {
                        console.log("Tarea actualizada:", data.message);
                    } else {
                        console.error("Error al actualizar la tarea:", data.error);
                    }
                },
                error: function(error) {
                    console.error("Error al realizar la solicitud:", error);
                }
            });
        }
        
    });
}



function guardarTarea() {
    let taskName = tasks[tasks.length - 1].name;
    let startDate = tasks[tasks.length - 1].start;
    let endDate = tasks[tasks.length - 1].end;

    let colorSelector = document.getElementById("colorSelector");
    let color = colorSelector.value;

    let newTask = {
        name: taskName,
        start: startDate,
        end: endDate,
        color: color
    };

    $.ajax({
        type: "POST",
        url: "/guardar_tarea",
        data: JSON.stringify(newTask),
        contentType: "application/json",
        dataType: "json",
        success: function(data) {
            if (data.id) {
                console.log("Tarea guardada con ID:", data.id);
            } else {
                console.error("Error al guardar la tarea:", data.error);
            }
        },
        error: function() {
            console.error("Error en la solicitud");
        }
    });
}

document.getElementById("colorSelector").addEventListener("input", function() {
    let color = this.value;
    let tasksWithCustomClass = document.querySelectorAll(`.task_bar.custom_class_${color}`);
    tasksWithCustomClass.forEach(function(taskElement) {
        let taskId = taskElement.getAttribute("data-task-id");
        let bar = gantt.get_bar(taskId);
        if (bar) {
            bar.custom_class = `custom_class_${taskId}_${color}`; 
            tasks[taskId - 1].color = color; 
        }
    });
});


function eliminarTareaSeleccionada() {
    let taskSelect = document.getElementById("taskSelect");
    let selectedTaskId = taskSelect.value; 

    if (selectedTaskId) {
        eliminarTarea(selectedTaskId); 
    } else {
        alert("Por favor, seleccione una tarea para eliminar.");
    }
}


cargarDiagrama();
