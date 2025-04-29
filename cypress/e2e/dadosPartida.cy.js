Cypress.Commands.add('deleteUsers', () => {
    return cy.exec('python delete_users.py', { failOnNonZeroExit: false }).then((result) => {
        console.log(result.stdout); 
        if (result.stderr) {
            console.error(result.stderr);
        } else {
            console.log('Usuários excluídos com sucesso');
        }
    });
});


Cypress.Commands.add('deleteGerenciador', () => {
    return cy.exec('python delete_gerenciadores.py', { failOnNonZeroExit: false }).then((result) => {
        console.log(result.stdout); 
        if (result.stderr) {
            console.error(result.stderr);
        } else {
            console.log('Gerenciadores excluídos com sucesso');
        }
    });
});


Cypress.Commands.add('deleteCompeticoes', () => {
    return cy.exec('python delete_competicoes.py', { failOnNonZeroExit: false }).then((result) => {
      console.log(result.stdout);
      if (result.stderr) {
        console.error(result.stderr);
      }
    });
});


  Cypress.Commands.add('signinGerenciador', () => {
    cy.visit('/');
    cy.get('.nav-links > :nth-child(1) > a').click();
    cy.get('#tipo_usuario');
    cy.get('select[name="tipo_usuario"]').select('Gerenciador');
    cy.get('#username').type('teste gerenciador');
    cy.get('#email').type('gerenciador@email.com');
    cy.get('#password1').type('12345');
    cy.get('#password2').type('12345');
    cy.get('.btn').click();
}); 


Cypress.Commands.add('loginGerenciador', () => {
    cy.get('#username').type('teste gerenciador');
    cy.get('#password').type('12345');
    cy.get('.btn').click();
});


Cypress.Commands.add('criarCompeticao', () => {
    cy.get('.card > .btn').click();
    cy.get('#nome').type('Competicao Cypress');
    cy.get('#numero_de_times').type('4');
    cy.get('#local').type('Recife');
    cy.get('button.btn').click();
});


Cypress.Commands.add('editarCompeticao', () => {
    cy.get('.card-actions > a.btn').click();
    cy.get('#nome').clear();
    cy.get('#nome').type('Edição Cypress');
    cy.get('#numero_de_times').clear();
    cy.get('#numero_de_times').type('6');
    cy.get('#local').clear();
    cy.get('#local').type('Olinda');
    cy.get('button.btn').click();

});


Cypress.Commands.add('criarTime', () => {
    cy.get('.card-actions > a.btn > .fas').click();
    cy.url().then((url) => {
      const regex = /editar(\d+)\/editar/;
      const match = url.match(regex);
  
      if (match) {
          const competicaoId = match[1];
          cy.log('ID da competição:', competicaoId);
  
          cy.get(`[href="/competicao/${competicaoId}/editar_times/"]`).click();
      } else {
          throw new Error('ID da competição não encontrado na URL!');
      }
  });
    cy.get('#nome').type('time Cypress');
    cy.get('.form-actions > .btn').click();
  });


Cypress.Commands.add('criarTime2', () => {
    cy.get('#nome').type('time Cypress2');
    cy.get('.form-actions > .btn').click();
  });
  

Cypress.Commands.add('criarPartida', () => {
    cy.url().then((url) => {
        const regex = /editar(\d+)\/editar/;
        const match = url.match(regex);
    
        if (match) {
            const competicaoId = match[1];
            cy.log('ID da competição:', competicaoId);
    
            cy.get(`[href="/competicao/${competicaoId}/partidas/"]`).click();
        } else {
            throw new Error('ID da competição não encontrado na URL!');
        }
    });
    cy.get('#time_casa');
    cy.get('select[name="time_casa"]').select('time Cypress');
    cy.get('#time_visitante');
    cy.get('select[name="time_visitante"]').select('time Cypress 2');
    cy.get('#data').type('2025-04-29');
    cy.get('#hora').type('16:00');
    cy.get('form > .form-actions > .btn').click();
    cy.wait(1500);

});


Cypress.Commands.add('editarPartida', () => {
    cy.get('a[href^="/partida/"][href$="/editar/"]').first() 
      .invoke('attr', 'href')
      .then((href) => {
        const id = href.split('/')[2];
        cy.log('ID capturado:', id);
        cy.get(`[href="/partida/${id}/editar/"]`).click(); 
        cy.get('#data').type('2025-05-03');
        cy.get('button.btn').click();
        cy.wait(1000);
      });
  });
  

Cypress.Commands.add('registrarDados', () => {
    cy.get('.btn-success').click();
    cy.get('form > :nth-child(2) > .form-control').type('3');
    cy.get('form > :nth-child(3) > .form-control').type('2');
    cy.get(':nth-child(5) > tbody > tr > :nth-child(2) > .form-control').type('3');
    cy.get(':nth-child(5) > tbody > tr > :nth-child(3) > .form-control').type('0');
    cy.get(':nth-child(5) > tbody > tr > :nth-child(4) > .form-control').type('1');
    cy.get(':nth-child(7) > tbody > tr > :nth-child(2) > .form-control').type('2');
    cy.get(':nth-child(7) > tbody > tr > :nth-child(3) > .form-control').type('0');
    cy.get(':nth-child(7) > tbody > tr > :nth-child(4) > .form-control').type('0');
    cy.get(':nth-child(7) > tbody > tr > :nth-child(5) > .form-control').type('1');
    cy.get('.btn-success').click();
});


describe('Registro de Dados', () => {

    beforeEach(() => {
        cy.clearCookies();
        cy.clearLocalStorage();
        cy.visit('/');
    });


    it('Cenario 1:Registrar os dados com sucesso ', () => {
        cy.get('.nav-links > :nth-child(2)').click();
        cy.loginGerenciador();
        cy.get('.card-actions > a.btn').click();
        cy.criarPartida();
        cy.editarPartida();
        cy.registrarDados();
        cy.get(':nth-child(4) > .btn').click();   
    
    });
});