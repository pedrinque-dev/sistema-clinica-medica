document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("calendario-container");
  if (!container) return;

  const consultas = JSON.parse(
    document.getElementById("consultas-data").textContent,
  );

  const consultasPorDia = {};
  consultas.forEach(function (consulta) {
    if (!consultasPorDia[consulta.data]) {
      consultasPorDia[consulta.data] = [];
    }
    consultasPorDia[consulta.data].push(consulta);
  });

  const hoje = new Date();
  let mesAtual = hoje.getMonth();
  let anoAtual = hoje.getFullYear();

  const nomesMeses = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
  ];
  const nomesDiasSemana = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];

  function formatarDataISO(ano, mes, dia) {
    const mesFormatado = String(mes + 1).padStart(2, "0");
    const diaFormatado = String(dia).padStart(2, "0");
    return `${ano}-${mesFormatado}-${diaFormatado}`;
  }

  function escapeHtml(texto) {
    const div = document.createElement("div");
    div.textContent = texto;
    return div.innerHTML;
  }

  function renderizarCalendario() {
    const primeiroDiaDoMes = new Date(anoAtual, mesAtual, 1);
    const ultimoDiaDoMes = new Date(anoAtual, mesAtual + 1, 0);
    const diaDaSemanaInicial = primeiroDiaDoMes.getDay();
    const totalDiasNoMes = ultimoDiaDoMes.getDate();

    let html = `
            <div class="calendario-header">
                <button type="button" class="btn btn-outline-secondary btn-sm" id="btn-mes-anterior">&laquo;</button>
                <h5 class="mb-0">${nomesMeses[mesAtual]} de ${anoAtual}</h5>
                <button type="button" class="btn btn-outline-secondary btn-sm" id="btn-mes-seguinte">&raquo;</button>
            </div>
            <div class="calendario-grid calendario-dias-semana">
        `;

    nomesDiasSemana.forEach(function (nomeDia) {
      html += `<div class="calendario-dia-semana">${nomeDia}</div>`;
    });
    html += `</div><div class="calendario-grid">`;

    for (let i = 0; i < diaDaSemanaInicial; i++) {
      html += `<div class="calendario-celula calendario-celula-vazia"></div>`;
    }

    for (let dia = 1; dia <= totalDiasNoMes; dia++) {
      const dataISO = formatarDataISO(anoAtual, mesAtual, dia);
      const consultasDoDia = consultasPorDia[dataISO] || [];
      const temConsulta = consultasDoDia.length > 0;

      html += `
                <div class="calendario-celula ${temConsulta ? "calendario-celula-com-consulta" : ""}" data-data="${dataISO}">
                    <span class="calendario-numero-dia">${dia}</span>
                    ${temConsulta ? `<span class="badge text-bg-primary calendario-badge">${consultasDoDia.length}</span>` : ""}
                </div>
            `;
    }

    html += `</div>`;
    container.innerHTML = html;

    document
      .getElementById("btn-mes-anterior")
      .addEventListener("click", function () {
        mesAtual--;
        if (mesAtual < 0) {
          mesAtual = 11;
          anoAtual--;
        }
        renderizarCalendario();
      });

    document
      .getElementById("btn-mes-seguinte")
      .addEventListener("click", function () {
        mesAtual++;
        if (mesAtual > 11) {
          mesAtual = 0;
          anoAtual++;
        }
        renderizarCalendario();
      });

    container
      .querySelectorAll(".calendario-celula-com-consulta")
      .forEach(function (celula) {
        celula.addEventListener("click", function () {
          const dataClicada = celula.getAttribute("data-data");
          exibirConsultasDoDia(dataClicada);
        });
      });
  }

  function exibirConsultasDoDia(dataISO) {
    const listaContainer = document.getElementById("lista-consultas-dia");
    const consultasDoDia = consultasPorDia[dataISO] || [];

    const [ano, mes, dia] = dataISO.split("-");
    let html = `<h6>Consultas em ${dia}/${mes}/${ano}</h6>`;

    if (consultasDoDia.length === 0) {
      html += `<p class="text-muted">Nenhuma consulta neste dia.</p>`;
    } else {
      html += `<ul class="list-group">`;
      consultasDoDia.forEach(function (consulta) {
        html += `
           <li class="list-group-item">
               <strong>${consulta.horario}</strong> — ${escapeHtml(consulta.paciente)} com ${escapeHtml(consulta.medico)}
              <span class="badge text-bg-secondary float-end">${escapeHtml(consulta.status)}</span>
           </li>
        `;
      });
      html += `</ul>`;
    }

    listaContainer.innerHTML = html;
  }

  renderizarCalendario();
});
