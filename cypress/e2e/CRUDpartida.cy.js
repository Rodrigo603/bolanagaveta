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
    cy.get('#endereco_descritivo').type('Rua Dr. Enéas de Lucena 120,Rosarinho - Recife/PE');
    cy.get('.btn-sm').click();
    cy.get('.form-actions > button.btn').click();
    cy.get('#latitude').type('-8.0331457');
    cy.get('#longitude').type('-34.8950922');
    cy.get('.form-actions > button.btn').click();
});



Cypress.Commands.add('editarCompeticao', () => {
    cy.get('.card-actions > a.btn').click();
    cy.get('#nome').clear();
    cy.get('#nome').type('Edição Cypress');
    cy.get('#numero_de_times').clear();
    cy.get('#numero_de_times').type('6');
    cy.get('#endereco_descritivo').clear();
    cy.get('#endereco_descritivo').type('Estrada de Belem 272,Encruzilhada - Recife/PE');
    cy.get('#latitude').clear();
    cy.get('#latitude').type('-8.03625');
    cy.get('#longitude').clear();
    cy.get('#longitude').type('-34.88941');
    cy.get('.btn-primary').click();

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
    cy.get('.btn-secondary').click();
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
    cy.get('select[name="time_visitante"]').select('time Cypress2');
    cy.get('#data').type('2025-04-29');
    cy.get('#hora').type('16:00');
    cy.get('form > .form-actions > .btn').click();
    cy.wait(1500);

});

Cypress.Commands.add('criarPartidaIncompleta', () => {
    cy.get('.btn-secondary').click();
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
    cy.get('select[name="time_visitante"]').select('time Cypress2');
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
  

describe('CRUD de partidas', () => {

    beforeEach(() => {
        cy.deleteUsers()
          .then(() => cy.deleteCompeticoes())
          .then(() => {
              cy.clearCookies();
              cy.clearLocalStorage();
              cy.visit('/');
    });
});


    it('Cenario 1: Criação de partida bem sucedida', () => {
        cy.signinGerenciador();
        cy.loginGerenciador();
        cy.criarCompeticao();
        cy.editarCompeticao();
        cy.criarTime();
        cy.criarTime2();
        cy.criarPartida();
    });


    it('Cenario 2: Criação de partida com dados incompletos' , () => {
        cy.signinGerenciador();
        cy.loginGerenciador();
        cy.criarCompeticao();
        cy.editarCompeticao();
        cy.criarTime();
        cy.criarTime2();
        cy.criarPartidaIncompleta();
    });


    it('Cenario 3: Editar uma partida', () => {
        cy.signinGerenciador();
        cy.loginGerenciador();
        cy.criarCompeticao();
        cy.editarCompeticao();
        cy.criarTime();
        cy.criarTime2();
        cy.criarPartida();
        cy.editarPartida();
    });
});