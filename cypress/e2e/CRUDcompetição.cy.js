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


Cypress.Commands.add('criarCompeticaoIncompleta', () => {
    cy.get('.card > .btn').click();
    cy.get('#numero_de_times').type('4');
    cy.get('#endereco_descritivo').type('Estrada de Belem 272,Encruzilhada - Recife/PE');
    cy.get('.form-actions > button.btn').click();
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
    cy.get('#endereco_descritivo').clear();
    cy.get('#endereco_descritivo').type('Estrada de Belem 272,Encruzilhada - Recife/PE');
    cy.get('#latitude').clear();
    cy.get('#latitude').type('-8.03625');
    cy.get('#longitude').clear();
    cy.get('#longitude').type('-34.88941');
    cy.get('.btn-primary').click();

});

describe('CRUD da competicao', () => {

    beforeEach(() => {
        cy.deleteUsers()
          .then(() => cy.deleteCompeticoes())
          .then(() => {
              cy.clearCookies();
              cy.clearLocalStorage();
              cy.visit('/');
        });
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