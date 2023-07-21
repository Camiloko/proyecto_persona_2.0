        const tasks = [];

        function agregarTarea() {
            const taskName = document.getElementById("taskName").value;
            const startDate = document.getElementById("startDate").value;
            const endDate = document.getElementById("endDate").value;

            if (taskName && startDate && endDate) {
                tasks.push({
                    id: tasks.length + 1,
                    name: taskName,
                    start: new Date(startDate),
                    end: new Date(endDate),
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
            const ganttContainer = document.getElementById("ganttChart");
            ganttContainer.innerHTML = "";

            const gantt = new Gantt(ganttContainer, tasks, {
                header_height: 50,
                column_width: 30,
                step: 24,
                view_modes: ['Quarter Day', 'Half Day', 'Day', 'Week', 'Month'],
                bar_height: 20,
                bar_corner_radius: 3,
                arrow_curve: 5,
                padding: 18,
                view_mode: 'Week',
                date_format: 'YYYY-MM-DD',
                custom_popup_html: function (task) {
                    return '<div class="details-container">' +
                        '<h5>' + task.name + '</h5>' +
                        '<p>Fecha de Inicio: ' + task._start.format('YYYY-MM-DD') + '</p>' +
                        '<p>Fecha de Finalización: ' + task._end.format('YYYY-MM-DD') + '</p>' +
                        '</div>';
                }
            });

            gantt.change_view_mode('Week');
        }

        function cambiarModoVisualizacion() {
            const viewMode = document.getElementById("viewMode").value;
            const ganttContainer = document.getElementById("ganttChart");
            ganttContainer.innerHTML = "";
            const gantt = new Gantt(ganttContainer, tasks, {
                view_mode: viewMode,
                date_format: 'YYYY-MM-DD',
                custom_popup_html: function (task) {
                    return '<div class="details-container">' +
                        '<h5>' + task.name + '</h5>' +
                        '<p>Fecha de Inicio: ' + task._start.format('YYYY-MM-DD') + '</p>' +
                        '<p>Fecha de Finalización: ' + task._end.format('YYYY-MM-DD') + '</p>' +
                        '</div>';
                }
            });
        }

        function cambiarFechaVista() {
            const viewStart = document.getElementById("viewStart").value;
            const viewEnd = document.getElementById("viewEnd").value;
            const ganttContainer = document.getElementById("ganttChart");
            ganttContainer.innerHTML = "";
            const gantt = new Gantt(ganttContainer, tasks, {
                view_mode: 'custom',
                date_format: 'YYYY-MM-DD',
                custom_popup_html: function (task) {
                    return '<div class="details-container">' +
                        '<h5>' + task.name + '</h5>' +
                        '<p>Fecha de Inicio: ' + task._start.format('YYYY-MM-DD') + '</p>' +
                        '<p>Fecha de Finalización: ' + task._end.format('YYYY-MM-DD') + '</p>' +
                        '</div>';
                },
                start_date: viewStart,
                end_date: viewEnd
            });
        }
        function mostrarTutorial() {
            const tutorialModal = document.getElementById("tutorialModal");
            tutorialModal.style.display = "block";
        }

        window.addEventListener("load", function () {
            const tutorialModal = document.getElementById("tutorialModal");
            const closeButton = tutorialModal.querySelector(".close");

            closeButton.addEventListener("click", function () {
                tutorialModal.style.display = "none";
            });

            window.addEventListener("click", function (event) {
                if (event.target === tutorialModal) {
                    tutorialModal.style.display = "none";
                }
            });
        });