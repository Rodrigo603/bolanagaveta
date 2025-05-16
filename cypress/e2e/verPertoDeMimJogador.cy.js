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


Cypress.Commands.add('criarCompeticao2', () => {
    cy.get('#nome').type('Competicao Cypress 2');
    cy.get('#numero_de_times').type('4');
    cy.get('#endereco_descritivo').type('Rua Arnoldo magalhães,Casa Amarela - Recife/PE');
    cy.get('.btn-sm').click();
    cy.get('.form-actions > button.btn').click();
    cy.get('#latitude').type('-8.0267995');
    cy.get('#longitude').type('-34.9094749');
    cy.get('.form-actions > button.btn').click();
});


describe('Visualização de competições perto do jogador', () => {

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
    it("Cenario 1: Visualização das competições com sucesso", () => {
        cy.signinGerenciador();
        cy.loginGerenciador();
        cy.criarCompeticao();
        cy.get('.page-header > .btn').click();
        cy.criarCompeticao2();
        cy.get('.nav-links > :nth-child(3) > a').click();
        cy.get('.nav-links > :nth-child(1) > a').click();
        cy.signinJogador();
        cy.loginJogador();
        cy.get(':nth-child(3) > .card-body > .btn').click();
        cy.get('.btn').click();
        cy.wait(2000);
    }); 
    
    it('Cenario 2: Visualizção sem competições por perto', () => {
        cy.signinJogador();
        cy.loginJogador();
        cy.get(':nth-child(3) > .card-body > .btn').click();
        cy.get('.btn').click();
        cy.wait(1000);
    });


});