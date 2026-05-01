// Auto-dismiss messages after 5 seconds
document.addEventListener('DOMContentLoaded', () => {
  const msgs = document.querySelectorAll('.message');
  msgs.forEach(msg => {
    setTimeout(() => {
      msg.style.opacity = '0';
      msg.style.transition = 'opacity 0.5s';
      setTimeout(() => msg.remove(), 500);
    }, 5000);
  });
});
