Cypress.Commands.add('deleteUsers', () => {
    return cy.exec('python delete_users.py', { failOnNonZeroExit: false }).then((result) => {
      console.log(result.stdout);
      if (result.stderr) {
        console.error(result.stderr);
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


Cypress.Commands.add('deleteTimes', () => {
    return cy.exec('python delete_times.py', { failOnNonZeroExit: false }).then((result) => {
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
  cy.wait(1000);
});


Cypress.Commands.add('excluirTime', () => {
  cy.get('.team-delete-form > .btn').click();
  cy.wait(1000);
});


Cypress.Commands.add('criarTimeRepetido', () => {
  cy.get('#nome').type('time Cypress');
  cy.get('.form-actions > .btn').click();
  cy.wait(1000);
});


describe('CRUD de times', () => {
    
      

    beforeEach(() => {
        cy.deleteUsers()
          .then(() => cy.deleteCompeticoes())
          .then(() => cy.deleteTimes())
          .then(() => {
              cy.clearCookies();
              cy.clearLocalStorage();
              cy.visit('/');
          });
    });

    
    it('Cenario 1: Criar o time e visualizá-lo com sucesso.', () => {
        cy.signinGerenciador();
        cy.loginGerenciador();
        cy.criarCompeticao();
        cy.criarTime();
    });


    it('Cenario 2: : Cadastro de time já existente', () => {
        cy.signinGerenciador();
        cy.loginGerenciador();
        cy.criarCompeticao();
        cy.criarTime();
        cy.criarTimeRepetido();
    });
    
    
    it('Cenario 3: Excluir Competição', () => {
       cy.signinGerenciador();
       cy.loginGerenciador();
       cy.criarCompeticao();
       cy.criarTime();
       cy.excluirTime();
    });

});
