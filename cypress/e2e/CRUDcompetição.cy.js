Cypress.Commands.add('deleteUsers', () => {
    cy.exec('python delete_users.py', { failOnNonZeroExit: false }).then((result) => {
      console.log(result.stdout); 
      if (result.stderr) {
        console.error(result.stderr);
      }
    });
  });


Cypress.Commands.add('deleteCompeticoes', () => {
    cy.exec('python delete_competicoes.py', { failOnNonZeroExit: false }).then((result) => {
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


Cypress.Commands.add('criarCompeticaoIncompleta', () => {
    cy.get('.card > .btn').click();
    cy.get('#numero_de_times').type('4');
    cy.get('#local').type('Recife');
    cy.get('button.btn').click();
});


Cypress.Commands.add('excluirCompeticao', () => {
    cy.wait(1000);
    cy.get('form > .btn').click();
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

describe('CRUD da competicao', () => {

    beforeEach(() => {
        cy.deleteUsers();
        cy.deleteCompeticoes();
    });

    it('Cenario 1: Criar a competição e visualizá-la com sucesso.', () => {
        cy.signinGerenciador();
        cy.loginGerenciador();
        cy.criarCompeticao();
        cy.wait(1000);
    });
    
    it('Cenario 2: Excluir a competição.', () => {
        cy.signinGerenciador();
        cy.loginGerenciador();
        cy.criarCompeticao();
        cy.excluirCompeticao();
        cy.wait(1000);

    });
    it('Cenario 3: Editar a competição', () => {
        cy.signinGerenciador();
        cy.loginGerenciador();
        cy.criarCompeticao();
        cy.editarCompeticao();
    });
    it('cenario 4: Tentar cadastrar sem colocar todas as informações' , () => {
        cy.signinGerenciador();
        cy.loginGerenciador();
        cy.criarCompeticaoIncompleta();
        cy.wait(1000);
    });

});