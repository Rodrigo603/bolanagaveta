Cypress.Commands.add('deleteUsers', () => {
    return cy.exec('python delete_users.py', { failOnNonZeroExit: false }).then((result) => {
      console.log(result.stdout); 
      if (result.stderr) {
        console.error(result.stderr);
      }
    });
  });
 

  Cypress.Commands.add('deleteJogadores', () => {
    return cy.exec('python delete_jogadores.py', { failOnNonZeroExit: false }).then((result) => {
      console.log(result.stdout); 
      if (result.stderr) {
        console.error(result.stderr);
      }
    });
  });


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


Cypress.Commands.add('loginJogador', () => {
    cy.get('#username').type('teste jogador');
    cy.get('#password').type('12345');
    cy.get('.btn').click();
  });

  
describe('jogador flow', () => {

  before(() => {
    cy.deleteJogadores(); 
  });

 it('deve criar um usuario e fazer login no site', () => {
    cy.signinJogador();
    cy.loginJogador();
  });
});