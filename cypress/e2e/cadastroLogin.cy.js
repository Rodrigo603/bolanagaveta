Cypress.Commands.add('deleteUsers', () => {
    cy.exec('python delete_users.py', { failOnNonZeroExit: false }).then((result) => {
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

Cypress.Commands.add('home', () => {
    cy.visit('/');
})

Cypress.Commands.add('signinJogador', () => {
    cy.visit('/');
    cy.get('.nav-links > :nth-child(1) > a').click();
    cy.get('#tipo_usuario');
    cy.get('select[name="tipo_usuario"]').select('Jogador');
    cy.get('#username').type('teste jogador');
    cy.get('#email').type('jogador@email.com');
    cy.get('#password1').type('12345');
    cy.get('#password2').type('12345');
    cy.get('.btn').click();
});

Cypress.Commands.add('loginGerenciador', () => {
    cy.get('#username').type('teste gerenciador');
    cy.get('#password').type('12345');
    cy.get('.btn').click();
});

Cypress.Commands.add('loginJogador', () => {
  cy.get('#username').type('teste jogador');
  cy.get('#password').type('12345');
  cy.get('.btn').click();
});

describe('gerenciador flow', () => {

    before(() => {
      cy.deleteUsers(); 
    });
  
    it('deve criar um usuario e fazer login no site', () => {
      cy.signinGerenciador();
      cy.loginGerenciador();
    });
  });
//
  //describe('jogador flow', () => {
//
  //  before(() => {
  //    cy.deleteUsers(); 
  //  });
  //
  //  it('deve criar um usuario e fazer login no site', () => {
  //    cy.signinJogador();
  //    cy.loginJogador();
  //  });
  //});