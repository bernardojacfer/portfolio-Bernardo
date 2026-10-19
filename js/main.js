
const form = document.getElementById('contact-form');

if (form) {
  form.addEventListener('submit', function (event) {
    event.preventDefault();

    const feedback = document.getElementById('form-feedback');
    const nome = document.getElementById('nome').value.trim();
    const email = document.getElementById('email').value.trim();
    const mensagem = document.getElementById('mensagem').value.trim();

    if (!nome || !email || !mensagem) {
      feedback.textContent = 'Preencha todos os campos antes de enviar.';
      feedback.className = 'feedback error';
      return;
    }

    feedback.textContent = 'Mensagem pronta para envio (back-end ainda não conectado).';
    feedback.className = 'feedback success';
    form.reset();
  });
}