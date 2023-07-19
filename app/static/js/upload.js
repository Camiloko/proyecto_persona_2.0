// static/js/upload.js
document.addEventListener('DOMContentLoaded', function () {
    const selectCategoria = document.getElementById('categoria');
    const tipoGraficoSection = document.getElementById('tipo_grafico_section');
    const selectTipoGrafico = document.getElementById('tipo_grafico');
    const columnasSection = document.getElementById('columnas_section');

    selectCategoria.addEventListener('change', function () {
        const categoriaSeleccionada = selectCategoria.value;
        tipoGraficoSection.style.display = 'none';
        columnasSection.style.display = 'none';
        selectTipoGrafico.innerHTML = '';
        columnasSection.innerHTML = '';

        if (categoriaSeleccionada === 'tendencias') {
            selectTipoGrafico.innerHTML = `
                <option value="">Seleccione un tipo de gráfico</option>
                <option value="area">Gráfico de Área</option>
                <option value="lineas">Gráfico de Líneas</option>
            `;

            selectTipoGrafico.addEventListener('change', function () {
                const tipoGraficoSeleccionado = selectTipoGrafico.value;
                if (tipoGraficoSeleccionado !== '') {
                    columnasSection.innerHTML = `
                        <label for="columna_x">Columna X (Fecha):</label>
                        <input type="text" class="form-control" name="columna_x" id="columna_x" required>
                        <br><br>
                        <label for="columna_y">Columna Y (Valor):</label>
                        <input type="text" class="form-control" name="columna_y" id="columna_y" required>
                    `;
                    columnasSection.style.display = '';
                } else {
                    columnasSection.style.display = 'none';
                }
            });
        } else if (categoriaSeleccionada === 'comparacion') {
            selectTipoGrafico.innerHTML = `
                <option value="">Seleccione un tipo de gráfico</option>
                <option value="barras">Gráfico de Barras</option>
            `;

            selectTipoGrafico.addEventListener('change', function () {
                const tipoGraficoSeleccionado = selectTipoGrafico.value;
                if (tipoGraficoSeleccionado === 'barras') {
                    columnasSection.innerHTML = `
                        <label for="columna_x">Columna X (Categorias):</label>
                        <input type="text" class="form-control" name="columna_x" id="columna_x" required>
                        <br><br>
                        <label for="columna_y">Columna Y (Valores):</label>
                        <input type="text" class="form-control" name="columna_y" id="columna_y" required>
                    `;

                    columnasSection.style.display = '';
                } else {
                    columnasSection.style.display = 'none';
                }
            });
        } else if (categoriaSeleccionada === 'relacion') {
            selectTipoGrafico.innerHTML = `
                <option value="">Seleccione un tipo de gráfico</option>
                <option value="dispersion">Gráfico de Dispersión</option>
            `;

            selectTipoGrafico.addEventListener('change', function () {
                const tipoGraficoSeleccionado = selectTipoGrafico.value;
                if (tipoGraficoSeleccionado !== '') {
                    columnasSection.innerHTML = `
                        <label for="columna_x">Columna X (Numerico):</label>
                        <input type="text" class="form-control" name="columna_x" id="columna_x" required>
                        <br><br>
                        <label for="columna_y">Columna Y (Numerico):</label>
                        <input type="text" class="form-control" name="columna_y" id="columna_y" required>
                    `;
                    columnasSection.style.display = '';
                } else {
                    columnasSection.style.display = 'none';
                }
            });
        }

        tipoGraficoSection.style.display = '';
    });
});
