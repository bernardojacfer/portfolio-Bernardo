// Formulário de contato: envia a mensagem para a API Flask (/api/mensagens).
// Depende de api.js.
const form = document.getElementById('contact-form');

if (form) {
  form.addEventListener('submit', async function (event) {
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

    feedback.textContent = 'Enviando...';
    feedback.className = 'feedback';

    try {
      await api('/api/mensagens', { metodo: 'POST', corpo: { nome, email, mensagem } });
      feedback.textContent = 'Mensagem enviada com sucesso! Obrigado pelo contato.';
      feedback.className = 'feedback success';
      form.reset();
    } catch (erro) {
      feedback.textContent = erro.message;
      feedback.className = 'feedback error';
    }
  });
}
