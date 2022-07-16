
const activePage = window.location.pathname;

const navLinks = document.querySelectorAll('nav a').forEach(link => {   

    if(link.href.includes(`${activePage}`)){
      link.classList.add('active');
    }
  });

  function learnMorebutton(){
    document.getElementById("moreLinks").style.display = "table";}

    function sentMassege(){
        document.getElementById("sent").style.display = "table";}