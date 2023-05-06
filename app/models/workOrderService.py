#Work order service.py
from models.workOrdersDbLinkService import *
from abc import ABC, abstractmethod

########################## Work order master interface -> two services ########################
class WorkOrderServiceInterface(ABC):
        
        @abstractmethod
        def getAllWorkOrders(self):
            pass

        @abstractmethod
        def workOrderAdd(self, request):
            pass

        @abstractmethod
        def getWorkOrderById(self, woid:int):
            pass
               
        # def menuAdd(self):
        #     pass
        
        # def getMenuItem(self):
        #     pass
        @abstractmethod
        def updateWorkOrder():
            pass

        @abstractmethod
        def workOrderDelete(self, session):
             pass
        
class WorkOrderService(WorkOrderServiceInterface):
    
    def __init__(self) -> None:
        self.WorkOrderDBInstance:WorkOrdersDbLinkInterface = WorkOrdersDbLink()

    def getAllWorkOrders(self):
        return self.WorkOrderDBInstance.getAllWorkOrders()
    
    def workOrderAdd(self, request) -> bool:

        items:int = len(request.form)/6
        print (f"total item tally: {items}")
        i:int=1
        while i <= items:
            newWorkOrder: WorkOrderListDataStructure = WorkOrderListDataStructure( 
                 request.form[f'{i}.name'], 
                 request.form[f'{i}.number'], 
                 request.form[f'{i}.itemdescription'], 
                 request.form[f'{i}.project'], 
                 request.form[f'{i}.quantity'], 
                 request.form[f'{i}.duedate'])
            self.WorkOrderDBInstance.addWorkOrder(newWorkOrder)
            i+=1
        return True
    
    def getWorkOrderById(self, woid:int):
        return self.WorkOrderDBInstance.getWorkOrderById(woid)
    
    # def getMenuItem(self, menuId):
    #     searchById = 'id'
    #     result = self.fTdatabaseInstance.searchFoodRecord(searchById, menuId)
    #     return result
    
    # def menuItemEdit(self, request):
    #     self.newItemEdit:MenuItemStructure =  MenuItemStructure( request.form['name'], request.form['URL'], request.form['price'])
    #     self.newItemId = request.form['id']
    #     self.fTdatabaseInstance.updateFoodRecord(self.newItemId, self.newItemEdit)

    def workOrderDelete(self, request, wonumber:int = ""):
        
        idList: int = []
        if wonumber != "": idList.append(wonumber)

        requestList = list(request.form.items())
        for key,value in requestList:
            if value == "on":
                idList.append(key.split('.')[0])

        print(idList)        
        self.WorkOrderDBInstance.deleteWorkOrderRecords(idList)
            
        return
        # if 'submitYes' in request.form:
        #     self.fTdatabaseInstance.deleteFoodRecord(self.newItemId)
        #     return True
        # elif 'submitNo' in request.form:
        #     return False

    def updateWorkOrder(self, request):
        
        formData = list(request.form.items())
        datalist: list[WorkOrderListDataDBStructure] = []
        print(formData)
        for key, value in formData:
            if key.endswith('.id'):
                i = key.split('.')[0]
                item:WorkOrderListDataDBStructure = WorkOrderListDataDBStructure(request.form.get(f'{i}.id'),
                                                                request.form.get(f'{i}.wonumber'),
                                                                request.form.get(f'{i}.itemnumber'),
                                                                request.form.get(f'{i}.itemdescription'),
                                                                request.form.get(f'{i}.project'),
                                                                request.form.get(f'{i}.quantity'),
                                                                request.form.get(f'{i}.duedate'))
                print("item:.....",item)
                datalist.append(item)
        print("datlist=:.....", datalist)

        self.WorkOrderDBInstance.updateWOlist(datalist)

        return True

__all__ = ['WorkOrderService', 'WorkOrderServiceInterface']